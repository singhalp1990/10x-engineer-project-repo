import styles from "./SharedComponents.module.css";

interface LoadingSpinnerProps {
  label?: string;
  size?: "sm" | "md" | "lg";
}

export default function LoadingSpinner({ label = "Loading...", size = "md" }: LoadingSpinnerProps) {
  return (
    <div className={styles.spinnerWrapper}>
      <div className={`${styles.spinner} ${styles[`spinner_${size}`]}`} />
      <span>{label}</span>
    </div>
  );
}