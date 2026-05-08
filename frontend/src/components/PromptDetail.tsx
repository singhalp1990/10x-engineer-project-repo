import { Prompt } from "./PromptCard";
import styles from "./PromptComponents.module.css";

interface PromptDetailProps {
  prompt: Prompt;
}

export default function PromptDetail({ prompt }: PromptDetailProps) {
  return (
    <section className={styles.detail}>
      <header className={styles.detailHeader}>
        <h2>{prompt.title}</h2>
        <div className={styles.tags}>
          {prompt.tags.map((tag) => (
            <span key={tag} className={styles.tag}>
              {tag}
            </span>
          ))}
        </div>
      </header>

      <div className={styles.detailBody}>
        <div className={styles.detailBlock}>
          <h4>Description</h4>
          <p>{prompt.description}</p>
        </div>

        <div className={styles.detailBlock}>
          <h4>Example</h4>
          <pre>{prompt.example}</pre>
        </div>

        <div className={styles.detailMeta}>
          <span>Created: {new Date(prompt.createdAt).toLocaleDateString()}</span>
        </div>
      </div>
    </section>
  );
}