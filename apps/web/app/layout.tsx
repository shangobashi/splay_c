import type { Metadata } from "next";
import "./globals.css";
import { Navigation } from "@/components/features/navigation";
import { Toaster } from "@/components/ui/toaster";

export const metadata: Metadata = {
  title: "Splay - AI-Powered Furniture Discovery",
  description:
    "Upload a room photo and discover shoppable furniture matches with AI-powered detection.",
};

export const dynamic = "force-dynamic";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="page-gradient min-h-screen">
        <Navigation />
        <main className="container mx-auto px-4 py-8">{children}</main>
        <Toaster />
      </body>
    </html>
  );
}
