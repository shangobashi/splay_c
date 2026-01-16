"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuthStore } from "@/lib/stores/auth-store";
import { useScanStore } from "@/lib/stores/scan-store";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useToast } from "@/components/ui/use-toast";
import { formatDate, formatCategory } from "@/lib/utils";
import { Loader2, Eye, Clock, CheckCircle2, XCircle, Scan } from "lucide-react";
import { cn } from "@/lib/utils";

export default function HistoryPage() {
  const router = useRouter();
  const { toast } = useToast();
  const { user } = useAuthStore();
  const { scanHistory, loadHistory } = useScanStore();

  const [isLoading, setIsLoading] = useState(true);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!user) {
      toast({
        title: "Authentication Required",
        description: "Please login to view your scan history",
      });
      router.push("/auth/login");
    }
  }, [user, router, toast]);

  // Load history on mount
  useEffect(() => {
    if (user) {
      loadHistory().finally(() => setIsLoading(false));
    }
  }, [user, loadHistory]);

  if (!user) {
    return null; // Will redirect
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold">Scan History</h1>
          <p className="text-muted-foreground">
            View your previous scans and results
          </p>
        </div>
        <Button asChild>
          <Link href="/scan">
            <Scan className="mr-2 h-4 w-4" />
            New Scan
          </Link>
        </Button>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="flex justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      )}

      {/* Empty State */}
      {!isLoading && scanHistory.length === 0 && (
        <Card>
          <CardContent className="py-12 text-center space-y-4">
            <Scan className="h-12 w-12 mx-auto text-muted-foreground" />
            <div>
              <h3 className="text-lg font-medium">No Scans Yet</h3>
              <p className="text-sm text-muted-foreground">
                Upload your first room photo to get started
              </p>
            </div>
            <Button asChild>
              <Link href="/scan">Start Scanning</Link>
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Scan List */}
      {!isLoading && scanHistory.length > 0 && (
        <div className="space-y-4">
          {scanHistory.map((scan) => (
            <Card key={scan.id} className="overflow-hidden">
              <div className="grid md:grid-cols-[200px_1fr] gap-4">
                {/* Thumbnail */}
                <div className="relative h-48 md:h-auto bg-muted">
                  {scan.image_url && (
                    <img
                      src={scan.image_url}
                      alt={`Scan from ${formatDate(scan.created_at)}`}
                      className="object-cover w-full h-full"
                    />
                  )}
                  {!scan.image_url && (
                    <div className="flex items-center justify-center h-full">
                      <Scan className="h-12 w-12 text-muted-foreground" />
                    </div>
                  )}
                </div>

                {/* Details */}
                <div className="p-6 space-y-4">
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <StatusIcon status={scan.status} />
                        <span
                          className={cn(
                            "text-sm font-medium capitalize",
                            scan.status === "done" && "text-green-600",
                            scan.status === "failed" && "text-destructive",
                            scan.status === "processing" && "text-primary"
                          )}
                        >
                          {scan.status}
                        </span>
                      </div>
                      <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <Clock className="h-3 w-3" />
                        {formatDate(scan.created_at)}
                      </div>
                    </div>
                    <Button asChild variant="outline" size="sm">
                      <Link href={`/scan?id=${scan.id}`}>
                        <Eye className="mr-2 h-4 w-4" />
                        View
                      </Link>
                    </Button>
                  </div>

                  {/* Items Summary */}
                  {scan.status === "done" && scan.items && scan.items.length > 0 && (
                    <div>
                      <p className="text-sm font-medium mb-2">
                        {scan.items.length} item{scan.items.length !== 1 && "s"} detected
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {scan.items.map((item) => (
                          <span
                            key={item.id}
                            className="inline-flex items-center px-2 py-1 rounded-md bg-secondary text-xs font-medium"
                          >
                            {formatCategory(item.category)}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Error Message */}
                  {scan.status === "failed" && scan.error && (
                    <p className="text-sm text-destructive">{scan.error}</p>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

function StatusIcon({ status }: { status: string }) {
  switch (status) {
    case "done":
      return <CheckCircle2 className="h-4 w-4 text-green-600" />;
    case "failed":
      return <XCircle className="h-4 w-4 text-destructive" />;
    case "processing":
      return <Loader2 className="h-4 w-4 animate-spin text-primary" />;
    default:
      return <Clock className="h-4 w-4 text-muted-foreground" />;
  }
}
