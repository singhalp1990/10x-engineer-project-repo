import { FormEvent, useState } from "react";
import { Prompt, Collection } from "../types";
import styles from "./PromptComponents.module.css";

interface PromptFormProps {
  collections?: Collection[];
  initialPrompt?: Prompt;
  submitLabel?: string;
  onSubmit: (prompt: Omit<Prompt, "createdAt">) => void;
  onCancel?: () => void;
}

export default function PromptForm({
  collections = [],
  initialPrompt,
  submitLabel = "Save prompt",
  onSubmit,
  onCancel
}: PromptFormProps) {
  const [title, setTitle] = useState(initialPrompt?.title ?? "");
  const [description, setDescription] = useState(initialPrompt?.description ?? "");
  const [example, setExample] = useState(initialPrompt?.example ?? "");
  const [tags, setTags] = useState(initialPrompt?.tags.join(", ") ?? "");
  const [collectionId, setCollectionId] = useState(initialPrompt?.collectionId ?? "");
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = () => {
    const nextErrors: Record<string, string> = {};
    if (!title.trim()) nextErrors.title = "Title is required.";
    if (!description.trim()) nextErrors.description = "Description is required.";
    if (!example.trim()) nextErrors.example = "Example is required.";
    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!validate()) return;

    onSubmit({
      id: initialPrompt?.id ?? crypto.randomUUID(),
      title: title.trim(),
      description: description.trim(),
      example: example.trim(),
      tags: tags
        .split(",")
        .map((tag) => tag.trim())
        .filter(Boolean),
      collectionId: collectionId || undefined
    });
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit} noValidate>
      <label>
        Title
        <input
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          required
          aria-invalid={Boolean(errors.title)}
          aria-describedby={errors.title ? "title-error" : undefined}
        />
        {errors.title && <span id="title-error" className={styles.errorText}>{errors.title}</span>}
      </label>

      <label>
        Description
        <textarea
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          required
          aria-invalid={Boolean(errors.description)}
          aria-describedby={errors.description ? "description-error" : undefined}
        />
        {errors.description && <span id="description-error" className={styles.errorText}>{errors.description}</span>}
      </label>

      <label>
        Example
        <textarea
          value={example}
          onChange={(event) => setExample(event.target.value)}
          required
          aria-invalid={Boolean(errors.example)}
          aria-describedby={errors.example ? "example-error" : undefined}
        />
        {errors.example && <span id="example-error" className={styles.errorText}>{errors.example}</span>}
      </label>

      <label>
        Tags
        <input
          value={tags}
          onChange={(event) => setTags(event.target.value)}
          placeholder="Prompt, AI, example"
        />
      </label>

      <label>
        Collection
        <select value={collectionId} onChange={(event) => setCollectionId(event.target.value)}>
          <option value="">No collection</option>
          {collections.map((collection) => (
            <option key={collection.id} value={collection.id}>
              {collection.name}
            </option>
          ))}
        </select>
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