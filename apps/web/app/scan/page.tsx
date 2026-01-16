"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/lib/stores/auth-store";
import { useScanStore } from "@/lib/stores/scan-store";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ImageUpload } from "@/components/features/image-upload";
import { ScanResults } from "@/components/features/scan-results";
import { useToast } from "@/components/ui/use-toast";
import { Loader2, ArrowRight } from "lucide-react";

export default function ScanPage() {
  const router = useRouter();
  const { toast } = useToast();
  const { user } = useAuthStore();
  const {
    currentScan,
    isLoading,
    isUploading,
    error,
    createScan,
    pollScan,
    clearError,
    clearCurrentScan,
  } = useScanStore();

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!user) {
      toast({
        title: "Authentication Required",
        description: "Please login to scan images",
      });
      router.push("/auth/login");
    }
  }, [user, router, toast]);

  // Handle errors
  useEffect(() => {
    if (error) {
      toast({
        variant: "destructive",
        title: "Scan Error",
        description: error,
      });
      clearError();
    }
  }, [error, toast, clearError]);

  const handleImageSelect = (file: File) => {
    setSelectedFile(file);
    setImagePreview(URL.createObjectURL(file));
    clearCurrentScan();
  };

  const handleScan = async () => {
    if (!selectedFile) return;

    try {
      const scanId = await createScan(selectedFile);

      toast({
        title: "Scan Started",
        description: "Processing your image...",
      });

      // Poll for results
      await pollScan(scanId);

      toast({
        title: "Scan Complete",
        description: "Your results are ready!",
      });
    } catch (err) {
      // Error handled by store and useEffect
    }
  };

  const handleNewScan = () => {
    setSelectedFile(null);
    setImagePreview(null);
    clearCurrentScan();
  };

  if (!user) {
    return null; // Will redirect
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-4xl font-bold">Scan Your Room</h1>
        <p className="text-muted-foreground">
          Upload a photo to discover furniture and get shoppable matches
        </p>
      </div>

      {/* Upload Section */}
      {!currentScan && (
        <Card>
          <CardHeader>
            <CardTitle>Upload Image</CardTitle>
            <CardDescription>
              Take or upload a photo of a room with furniture
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <ImageUpload
              onImageSelect={handleImageSelect}
              disabled={isUploading || isLoading}
            />
            {selectedFile && (
              <div className="flex justify-center">
                <Button
                  size="lg"
                  onClick={handleScan}
                  disabled={isUploading || isLoading}
                  className="gap-2"
                >
                  {isUploading || isLoading ? (
                    <>
                      <Loader2 className="h-5 w-5 animate-spin" />
                      {isUploading ? "Uploading..." : "Processing..."}
                    </>
                  ) : (
                    <>
                      Scan Image
                      <ArrowRight className="h-5 w-5" />
                    </>
                  )}
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Processing Status */}
      {isLoading && currentScan && currentScan.status === "processing" && (
        <Card>
          <CardContent className="py-8 text-center space-y-4">
            <Loader2 className="h-12 w-12 animate-spin mx-auto text-primary" />
            <div>
              <h3 className="text-lg font-medium">Processing Image</h3>
              <p className="text-sm text-muted-foreground">
                Our AI is detecting furniture items...
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Results */}
      {currentScan && (currentScan.status === "done" || currentScan.status === "failed") && (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">Results</h2>
            <Button onClick={handleNewScan} variant="outline">
              New Scan
            </Button>
          </div>
          <ScanResults scan={currentScan} imageUrl={imagePreview || undefined} />
        </div>
      )}
    </div>
  );
}
