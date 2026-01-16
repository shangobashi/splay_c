import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Scan, Sparkles, ShoppingBag, Shield } from "lucide-react";

export default function HomePage() {
  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center space-y-6 py-12">
        <h1 className="text-5xl font-bold tracking-tight sm:text-6xl">
          Shop The Room
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Upload a room photo and discover shoppable furniture matches with
          AI-powered detection. Find the perfect pieces for your space.
        </p>
        <div className="flex gap-4 justify-center">
          <Button asChild size="lg">
            <Link href="/scan">
              <Scan className="mr-2 h-5 w-5" />
              Start Scanning
            </Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link href="/auth/register">Sign Up Free</Link>
          </Button>
        </div>
      </section>

      {/* Features */}
      <section className="space-y-8">
        <h2 className="text-3xl font-bold text-center">How It Works</h2>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <FeatureCard
            icon={Scan}
            title="1. Upload Your Photo"
            description="Take or upload a photo of any room. Our AI works with any image quality."
          />
          <FeatureCard
            icon={Sparkles}
            title="2. AI Detection"
            description="Our advanced AI detects furniture items and analyzes their style and features."
          />
          <FeatureCard
            icon={ShoppingBag}
            title="3. Shop Matches"
            description="Browse curated product matches from top retailers with direct purchase links."
          />
        </div>
      </section>

      {/* Benefits */}
      <section className="space-y-8">
        <h2 className="text-3xl font-bold text-center">Why Choose Splay?</h2>
        <div className="grid gap-6 sm:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Budget-Friendly Options</CardTitle>
              <CardDescription>
                Find affordable alternatives alongside premium matches
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Every scan includes budget-friendly alternatives so you can find
                the perfect piece within your price range.
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Fast & Accurate</CardTitle>
              <CardDescription>
                Get results in seconds with industry-leading AI
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Our AI processes images in real-time with high accuracy,
                detecting multiple items simultaneously.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* CTA */}
      <section className="text-center space-y-6 py-12 border-t">
        <h2 className="text-3xl font-bold">Ready to Get Started?</h2>
        <p className="text-lg text-muted-foreground max-w-xl mx-auto">
          Join thousands of users discovering furniture they love with Splay.
        </p>
        <Button asChild size="lg">
          <Link href="/auth/register">Create Free Account</Link>
        </Button>
      </section>
    </div>
  );
}

interface FeatureCardProps {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  description: string;
}

function FeatureCard({ icon: Icon, title, description }: FeatureCardProps) {
  return (
    <Card>
      <CardHeader>
        <Icon className="h-10 w-10 mb-2 text-primary" aria-hidden="true" />
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground">{description}</p>
      </CardContent>
    </Card>
  );
}
