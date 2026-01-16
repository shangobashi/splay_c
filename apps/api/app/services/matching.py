"""Product matching service."""
from typing import List, Dict, Tuple
import numpy as np
import hashlib
from sqlalchemy.orm import Session

from app.models.product import Product


def generate_stub_embedding(text: str, dimension: int = 512) -> List[float]:
    """Generate a deterministic embedding vector from text.

    Args:
        text: Text to generate embedding from
        dimension: Embedding dimension

    Returns:
        List of floats representing the embedding
    """
    # Create deterministic embedding based on text hash
    hash_obj = hashlib.md5(text.encode())
    seed = int(hash_obj.hexdigest()[:8], 16)
    np.random.seed(seed)

    # Generate random vector
    embedding = np.random.randn(dimension)

    # Normalize to unit vector
    norm = np.linalg.norm(embedding)
    if norm > 0:
        embedding = embedding / norm

    return embedding.tolist()


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Cosine similarity score (0-1)
    """
    if not vec1 or not vec2:
        return 0.0

    arr1 = np.array(vec1)
    arr2 = np.array(vec2)

    dot_product = np.dot(arr1, arr2)
    norm1 = np.linalg.norm(arr1)
    norm2 = np.linalg.norm(arr2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(dot_product / (norm1 * norm2))


def find_matching_products(
    category: str,
    embedding: List[float],
    db: Session,
    limit: int = 20
) -> List[Tuple[Product, float]]:
    """Find products matching the given category and embedding.

    Args:
        category: Product category to search
        embedding: Item embedding vector
        db: Database session
        limit: Maximum number of matches to return

    Returns:
        List of (product, similarity_score) tuples
    """
    # Query products by category
    products = db.query(Product).filter(
        Product.category == category,
        Product.in_stock == True
    ).all()

    if not products:
        return []

    # Calculate similarity for each product
    matches = []
    for product in products:
        if product.embedding:
            # Embedding stored as dict with 'vector' key
            product_embedding = product.embedding.get('vector', [])
            if product_embedding:
                similarity = cosine_similarity(embedding, product_embedding)
                matches.append((product, similarity))

    # Sort by similarity score descending
    matches.sort(key=lambda x: x[1], reverse=True)

    return matches[:limit]


def rank_products(
    matches: List[Tuple[Product, float]],
    top_n: int = 6
) -> List[Dict]:
    """Rank products and select budget alternative.

    Args:
        matches: List of (product, similarity_score) tuples
        top_n: Number of top products to return (default 6: 5 regular + 1 budget)

    Returns:
        List of product dictionaries with ranking info
    """
    if not matches:
        return []

    # Take top 5 matches
    top_matches = matches[:5]

    # Find budget alternative
    # Criteria: ≥20% cheaper than top match, similarity ≥ 0.75
    budget_alternative = None
    if top_matches:
        top_price = top_matches[0][0].price
        min_price = top_price * 0.8  # 20% cheaper

        for product, similarity in matches[5:]:  # Skip top 5
            if product.price < min_price and similarity >= 0.75:
                budget_alternative = (product, similarity)
                break

    # Build ranked results
    results = []

    for rank, (product, similarity) in enumerate(top_matches, start=1):
        results.append({
            "product_id": product.id,
            "name": product.name,
            "brand": product.brand,
            "price": product.price,
            "currency": product.currency,
            "image_url": product.image_url,
            "retailer_name": product.retailer_name,
            "retailer_url": product.retailer_url,
            "affiliate_url": product.affiliate_url,
            "similarity_score": round(similarity, 3),
            "is_budget_alternative": False,
            "rank": rank
        })

    # Add budget alternative if found
    if budget_alternative:
        product, similarity = budget_alternative
        results.append({
            "product_id": product.id,
            "name": product.name,
            "brand": product.brand,
            "price": product.price,
            "currency": product.currency,
            "image_url": product.image_url,
            "retailer_name": product.retailer_name,
            "retailer_url": product.retailer_url,
            "affiliate_url": product.affiliate_url,
            "similarity_score": round(similarity, 3),
            "is_budget_alternative": True,
            "rank": 6
        })

    return results
