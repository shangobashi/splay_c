"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuthStore } from "@/lib/stores/auth-store";
import { Button } from "@/components/ui/button";
import { LogOut, Scan, History, Home } from "lucide-react";
import { cn } from "@/lib/utils";

/**
 * Main navigation component
 * Shows different links based on auth state
 */
export function Navigation() {
  const pathname = usePathname();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    window.location.href = "/";
  };

  return (
    <nav
      className="border-b bg-card/50 backdrop-blur supports-[backdrop-filter]:bg-card/50"
      role="navigation"
      aria-label="Main navigation"
    >
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link
            href="/"
            className="flex items-center space-x-2 focus-visible-ring rounded-md"
          >
            <span className="text-2xl font-bold tracking-tight">Splay</span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center gap-2">
            {user ? (
              <>
                <NavLink href="/" icon={Home} active={pathname === "/"}>
                  Home
                </NavLink>
                <NavLink
                  href="/scan"
                  icon={Scan}
                  active={pathname === "/scan"}
                >
                  Scan
                </NavLink>
                <NavLink
                  href="/history"
                  icon={History}
                  active={pathname === "/history"}
                >
                  History
                </NavLink>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleLogout}
                  className="gap-2"
                >
                  <LogOut className="h-4 w-4" />
                  <span className="hidden sm:inline">Logout</span>
                </Button>
              </>
            ) : (
              <>
                <NavLink href="/" icon={Home} active={pathname === "/"}>
                  Home
                </NavLink>
                <Button asChild variant="outline" size="sm">
                  <Link href="/auth/login">Login</Link>
                </Button>
                <Button asChild size="sm">
                  <Link href="/auth/register">Sign Up</Link>
                </Button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

interface NavLinkProps {
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  active: boolean;
  children: React.ReactNode;
}

function NavLink({ href, icon: Icon, active, children }: NavLinkProps) {
  return (
    <Link
      href={href}
      className={cn(
        "flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors focus-visible-ring",
        active
          ? "bg-secondary text-foreground"
          : "text-muted-foreground hover:bg-secondary/50 hover:text-foreground"
      )}
      aria-current={active ? "page" : undefined}
    >
      <Icon className="h-4 w-4" />
      <span className="hidden sm:inline">{children}</span>
    </Link>
  );
}
