import { ButtonHTMLAttributes, ReactNode } from "react";
import styles from "./SharedComponents.module.css";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
  children: ReactNode;
}

export default function Button({
  variant = "primary",
  size = "md",
  children,
  className = "",
  disabled,
  ...props
}: ButtonProps) {
  const variantClass = styles[`button_${variant}`];
  const sizeClass = styles[`button_${size}`];

  return (
    <button
      type="button"
      className={`${styles.button} ${variantClass} ${sizeClass} ${className}`}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
}