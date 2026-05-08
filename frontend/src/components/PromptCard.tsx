import styles from "./PromptComponents.module.css";

export interface Prompt {
  id: string;
  title: string;
  description: string;
  example: string;
  tags: string[];
  createdAt: string;
}

interface PromptCardProps {
  prompt: Prompt;
  onSelect?: (id: string) => void;
}

export default function PromptCard({ prompt, onSelect }: PromptCardProps) {
  return (
    <article
      className={styles.card}
      onClick={() => onSelect?.(prompt.id)}
      role={onSelect ? "button" : undefined}
      tabIndex={onSelect ? 0 : undefined}
      onKeyDown={(event) => {
        if (onSelect && (event.key === "Enter" || event.key === " ")) {
          onSelect(prompt.id);
        }
      }}
    >
      <div className={styles.cardHeader}>
        <h3>{prompt.title}</h3>
        <div className={styles.tags}>
          {prompt.tags.map((tag) => (
            <span key={tag} className={styles.tag}>
              {tag}
            </span>
          ))}
        </div>
      </div>
      <p className={styles.description}>{prompt.description}</p>
      <pre className={styles.example}>{prompt.example}</pre>
    </article>
  );
}