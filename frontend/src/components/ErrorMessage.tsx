import Button from "./Button";
import styles from "./SharedComponents.module.css";

interface ErrorMessageProps {
  title?: string;
  message: string;
  onRetry?: () => void;
}

export default function ErrorMessage({ title = "Something went wrong", message, onRetry }: ErrorMessageProps) {
  return (
    <div className={styles.errorMessage}>
      <div>
        <p className={styles.errorTitle}>{title}</p>
        <p className={styles.errorText}>{message}</p>
      </div>
      {onRetry && (
        <Button variant="secondary" size="sm" onClick={onRetry}>
          Retry
        </Button>
      )}
    </div>
  );
}