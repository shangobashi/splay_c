"use client";

import { useCallback, useState } from "react";
import { Upload, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface ImageUploadProps {
  onImageSelect: (file: File) => void;
  disabled?: boolean;
  className?: string;
}

/**
 * Drag & drop image upload component
 * Supports click to browse and drag & drop
 * Accessibility: keyboard navigation, screen reader support
 */
export function ImageUpload({
  onImageSelect,
  disabled,
  className,
}: ImageUploadProps) {
  const [dragActive, setDragActive] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFile = useCallback(
    (file: File) => {
      if (!file.type.startsWith("image/")) {
        return;
      }

      setSelectedFile(file);
      setPreview(URL.createObjectURL(file));
      onImageSelect(file);
    },
    [onImageSelect]
  );

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setDragActive(false);

      if (disabled) return;

      const file = e.dataTransfer.files?.[0];
      if (file) {
        handleFile(file);
      }
    },
    [disabled, handleFile]
  );

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      if (disabled) return;

      const file = e.target.files?.[0];
      if (file) {
        handleFile(file);
      }
    },
    [disabled, handleFile]
  );

  const handleClear = useCallback(() => {
    setSelectedFile(null);
    setPreview(null);
  }, []);

  return (
    <div className={cn("w-full", className)}>
      {preview ? (
        <div className="relative">
          <img
            src={preview}
            alt="Upload preview"
            className="w-full rounded-lg border border-border shadow-lg"
          />
          <Button
            type="button"
            variant="destructive"
            size="icon"
            className="absolute right-2 top-2"
            onClick={handleClear}
            disabled={disabled}
            aria-label="Remove image"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      ) : (
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={cn(
            "flex flex-col items-center justify-center rounded-lg border-2 border-dashed p-12 transition-colors",
            dragActive
              ? "border-primary bg-primary/5"
              : "border-border bg-muted/30",
            disabled && "cursor-not-allowed opacity-50"
          )}
        >
          <Upload
            className={cn(
              "mb-4 h-12 w-12 transition-colors",
              dragActive ? "text-primary" : "text-muted-foreground"
            )}
            aria-hidden="true"
          />
          <p className="mb-2 text-sm font-medium">
            {dragActive ? "Drop image here" : "Drag & drop an image"}
          </p>
          <p className="mb-4 text-xs text-muted-foreground">or</p>
          <label htmlFor="file-upload">
            <Button
              type="button"
              variant="outline"
              disabled={disabled}
              onClick={() => document.getElementById("file-upload")?.click()}
            >
              Browse Files
            </Button>
          </label>
          <input
            id="file-upload"
            type="file"
            accept="image/*"
            className="sr-only"
            onChange={handleChange}
            disabled={disabled}
            aria-label="Upload image file"
          />
        </div>
      )}
    </div>
  );
}
