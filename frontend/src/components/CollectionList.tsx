import type { Collection } from "../types";
import styles from "./CollectionComponents.module.css";

interface CollectionListProps {
  collections: Collection[];
  selectedCollectionId?: string;
  onSelectCollection?: (id: string) => void;
}

export default function CollectionList({
  collections,
  selectedCollectionId,
  onSelectCollection
}: CollectionListProps) {
  if (collections.length === 0) {
    return <div className={styles.emptyState}>No collections yet.</div>;
  }

  return (
    <div className={styles.list}>
      {collections.map((collection) => (
        <button
          key={collection.id}
          type="button"
          className={`${styles.card} ${collection.id === selectedCollectionId ? styles.activeCard : ""}`}
          onClick={() => onSelectCollection?.(collection.id)}
        >
          <div className={styles.cardHeader}>
            <h3>{collection.name}</h3>
            <span>{collection.promptCount} prompts</span>
          </div>
          {collection.description && <p>{collection.description}</p>}
        </button>
      ))}
    </div>
  );
}