import PromptCard, { Prompt } from "./PromptCard";
import styles from "./PromptComponents.module.css";

interface PromptListProps {
  prompts: Prompt[];
  onSelectPrompt?: (id: string) => void;
}

export default function PromptList({ prompts, onSelectPrompt }: PromptListProps) {
  if (prompts.length === 0) {
    return <div className={styles.emptyState}>No prompts available yet.</div>;
  }

  return (
    <div className={styles.grid}>
      {prompts.map((prompt) => (
        <PromptCard key={prompt.id} prompt={prompt} onSelect={onSelectPrompt} />
      ))}
    </div>
  );
}