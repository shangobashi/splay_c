"use client";

import { useMemo } from "react";
import { ExternalLink, Tag } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import type { Scan } from "@/lib/api";
import { formatPrice, formatCategory } from "@/lib/utils";
import { cn } from "@/lib/utils";

interface ScanResultsProps {
  scan: Scan;
  imageUrl?: string;
}

/**
 * Display scan results with detected items and product matches
 * Shows bounding boxes overlaid on image
 * Product cards with affiliate links
 */
export function ScanResults({ scan, imageUrl }: ScanResultsProps) {
  // Generate bounding box overlays
  const overlay = useMemo(() => {
    if (!scan.items?.length || !imageUrl) return null;

    return (
      <div className="absolute inset-0 pointer-events-none">
        {scan.items.map((item) => (
          <div
            key={item.id}
            className="absolute border-2 border-primary rounded-lg shadow-lg bg-primary/10 backdrop-blur-[2px]"
            style={{
              left: `${item.bbox.x * 100}%`,
              top: `${item.bbox.y * 100}%`,
              width: `${item.bbox.w * 100}%`,
              height: `${item.bbox.h * 100}%`,
            }}
            title={`${formatCategory(item.category)} (${Math.round(item.confidence * 100)}%)`}
            role="img"
            aria-label={`Detected ${formatCategory(item.category)} with ${Math.round(item.confidence * 100)}% confidence`}
          />
        ))}
      </div>
    );
  }, [scan.items, imageUrl]);

  return (
    <div className="space-y-6">
      {/* Image with overlays */}
      {imageUrl && (
        <div className="relative w-full max-w-3xl mx-auto">
          <img
            src={imageUrl}
            alt="Scanned room"
            className="w-full rounded-lg border border-border shadow-lg"
          />
          {overlay}
        </div>
      )}

      {/* Scan status */}
      <div className="text-center">
        <p className="text-sm text-muted-foreground">
          Status:{" "}
          <span
            className={cn(
              "font-medium",
              scan.status === "done" && "text-green-600",
              scan.status === "failed" && "text-destructive",
              scan.status === "processing" && "text-primary"
            )}
          >
            {scan.status}
          </span>
        </p>
      </div>

      {/* Error message */}
      {scan.status === "failed" && scan.error && (
        <Card className="border-destructive">
          <CardHeader>
            <CardTitle className="text-destructive">Scan Failed</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm">{scan.error}</p>
          </CardContent>
        </Card>
      )}

      {/* Detected items */}
      {scan.status === "done" && scan.items && scan.items.length > 0 && (
        <div className="space-y-6">
          <h2 className="text-2xl font-bold">Detected Items</h2>
          {scan.items.map((item) => (
            <Card key={item.id}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="capitalize">
                    {formatCategory(item.category)}
                  </CardTitle>
                  <span className="text-sm text-muted-foreground">
                    {Math.round(item.confidence * 100)}% confidence
                  </span>
                </div>
                <CardDescription>
                  {item.matches.length} product{item.matches.length !== 1 && "s"} found
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {item.matches.map((match) => (
                    <ProductCard
                      key={match.rank}
                      product={match.product}
                      rank={match.rank}
                      isBudget={match.is_budget}
                    />
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* No items found */}
      {scan.status === "done" && (!scan.items || scan.items.length === 0) && (
        <Card>
          <CardHeader>
            <CardTitle>No Items Detected</CardTitle>
            <CardDescription>
              We couldn't detect any furniture in this image. Try uploading a
              clearer photo with better lighting.
            </CardDescription>
          </CardHeader>
        </Card>
      )}
    </div>
  );
}

interface ProductCardProps {
  product: {
    id: string;
    name: string;
    brand: string;
    price: number;
    affiliate_url: string;
  };
  rank: number;
  isBudget: boolean;
}

function ProductCard({ product, rank, isBudget }: ProductCardProps) {
  return (
    <Card className={cn(isBudget && "border-accent bg-accent/5")}>
      <CardHeader className="pb-3">
        {isBudget && (
          <div className="flex items-center gap-1 text-xs font-medium text-accent">
            <Tag className="h-3 w-3" />
            Budget Pick
          </div>
        )}
        <CardTitle className="text-base leading-tight">
          {product.name}
        </CardTitle>
        <CardDescription className="text-xs">{product.brand}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        <div>
          <p className="text-lg font-bold">{formatPrice(product.price)}</p>
          <p className="text-xs text-muted-foreground">Rank {rank}</p>
        </div>
        <Button
          asChild
          variant="outline"
          size="sm"
          className="w-full gap-2"
        >
          <a
            href={product.affiliate_url}
            target="_blank"
            rel="noopener noreferrer"
            aria-label={`View ${product.name} on retailer site`}
          >
            View Product
            <ExternalLink className="h-3 w-3" />
          </a>
        </Button>
      </CardContent>
    </Card>
  );
}
