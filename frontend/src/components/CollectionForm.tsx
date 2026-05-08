import { FormEvent, useState } from "react";
import type { Collection } from "../types";
import styles from "./CollectionComponents.module.css";

interface CollectionFormProps {
  initialCollection?: Omit<Collection, "promptCount">;
  submitLabel?: string;
  onSubmit: (collection: Omit<Collection, "promptCount">) => void;
  onCancel?: () => void;
}

export default function CollectionForm({
  initialCollection,
  submitLabel = "Create collection",
  onSubmit,
  onCancel
}: CollectionFormProps) {
  const [name, setName] = useState(initialCollection?.name ?? "");
  const [description, setDescription] = useState(initialCollection?.description ?? "");
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = () => {
    const nextErrors: Record<string, string> = {};
    if (!name.trim()) nextErrors.name = "Collection name is required.";
    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!validate()) return;

    onSubmit({
      id: initialCollection?.id ?? crypto.randomUUID(),
      name: name.trim(),
      description: description.trim() || undefined
    });
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit} noValidate>
      <label>
        Collection name
        <input
          value={name}
          onChange={(event) => setName(event.target.value)}
          required
          aria-invalid={Boolean(errors.name)}
          aria-describedby={errors.name ? "name-error" : undefined}
        />
        {errors.name && <span id="name-error" className={styles.errorText}>{errors.name}</span>}
      </label>

      <label>
        Description
        <textarea
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          placeholder="Optional description"
        />
      </label>

      <div className={styles.formActions}>
        <button type="submit" className={styles.primaryButton}>
          {submitLabel}
        </button>
        {onCancel && (
          <button type="button" className={styles.secondaryButton} onClick={onCancel}>
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}