import { useEffect, useMemo, useState } from "react";
import Layout from "./components/Layout";
import PromptList from "./components/PromptList";
import PromptDetail from "./components/PromptDetail";
import PromptForm from "./components/PromptForm";
import CollectionList from "./components/CollectionList";
import CollectionForm from "./components/CollectionForm";
import Button from "./components/Button";
import Modal from "./components/Modal";
import SearchBar from "./components/SearchBar";
import LoadingSpinner from "./components/LoadingSpinner";
import ErrorMessage from "./components/ErrorMessage";
import { Prompt, Collection } from "./types";
import * as api from "./api/api";
import styles from "./App.module.css";

function App() {
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [collections, setCollections] = useState<Collection[]>([]);
  const [selectedPromptId, setSelectedPromptId] = useState<string | null>(null);
  const [selectedCollectionId, setSelectedCollectionId] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showPromptModal, setShowPromptModal] = useState(false);
  const [promptToEdit, setPromptToEdit] = useState<Prompt | null>(null);
  const [showCollectionModal, setShowCollectionModal] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const selectedPrompt = useMemo(
    () => prompts.find((prompt) => prompt.id === selectedPromptId) ?? null,
    [prompts, selectedPromptId]
  );

  const loadCollections = async () => {
    try {
      const data = await api.getCollections();
      setCollections(data);
    } catch (err) {
      setError((err as Error).message || "Unable to load collections");
    }
  };

  const loadPrompts = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await api.getPrompts(selectedCollectionId ?? undefined, searchTerm || undefined);
      setPrompts(data);
      if (selectedPromptId && !data.some((prompt) => prompt.id === selectedPromptId)) {
        setSelectedPromptId(null);
      }
    } catch (err) {
      setError((err as Error).message || "Unable to load prompts");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadCollections();
    loadPrompts();
  }, []);

  useEffect(() => {
    loadPrompts();
  }, [selectedCollectionId]);

  const handlePromptSave = async (prompt: Omit<Prompt, "createdAt">) => {
    setIsLoading(true);
    setError(null);

    try {
      const saved = prompt.id && prompts.some((item) => item.id === prompt.id)
        ? await api.updatePrompt(prompt.id, prompt)
        : await api.createPrompt(prompt);

      setPrompts((current) => {
        const exists = current.some((item) => item.id === saved.id);
        if (exists) {
          return current.map((item) => (item.id === saved.id ? saved : item));
        }
        return [saved, ...current];
      });

      if (!collections.some((collection) => collection.id === saved.collectionId)) {
        await loadCollections();
      }

      setSelectedPromptId(saved.id);
      setShowPromptModal(false);
      setPromptToEdit(null);
    } catch (err) {
      setError((err as Error).message || "Unable to save prompt");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeletePrompt = async () => {
    if (!selectedPromptId) return;
    setIsLoading(true);
    setError(null);

    try {
      await api.deletePrompt(selectedPromptId);
      setPrompts((current) => current.filter((prompt) => prompt.id !== selectedPromptId));
      setSelectedPromptId(null);
      setShowDeleteConfirm(false);
    } catch (err) {
      setError((err as Error).message || "Unable to delete prompt");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Layout>
      <div className={styles.dashboard}>
        <div className={styles.pageHeader}>
          <div>
            <h1>Prompt Dashboard</h1>
            <p>Manage prompts, collections, and review prompt details.</p>
          </div>
          <div className={styles.actions}>
            <Button onClick={() => setShowCollectionModal(true)}>New collection</Button>
            <Button variant="secondary" onClick={() => {
              setPromptToEdit(null);
              setShowPromptModal(true);
            }}>
              New prompt
            </Button>
          </div>
        </div>

        <div className={styles.searchRow}>
          <SearchBar
            value={searchTerm}
            onChange={setSearchTerm}
            onSearch={loadPrompts}
            placeholder="Search prompts..."
          />
        </div>

        {error && <ErrorMessage message={error} onRetry={loadPrompts} />}

        <div className={styles.grid}>
          <section className={styles.collectionsPane}>
            <div className={styles.sectionHeader}>
              <h2>Collections</h2>
            </div>
            <CollectionList
              collections={collections}
              selectedCollectionId={selectedCollectionId ?? undefined}
              onSelectCollection={(id) =>
                setSelectedCollectionId((current) => (current === id ? null : id))
              }
            />
          </section>

          <section className={styles.promptsPane}>
            <div className={styles.sectionHeader}>
              <h2>Prompts</h2>
            </div>

            {isLoading ? (
              <LoadingSpinner label="Loading prompts..." />
            ) : (
              <PromptList
                prompts={prompts}
                onSelectPrompt={(id) => {
                  setSelectedPromptId(id);
                  setPromptToEdit(null);
                }}
              />
            )}

            <div className={styles.detailArea}>
              {selectedPrompt ? (
                <div className={styles.detailCard}>
                  <PromptDetail prompt={selectedPrompt} />
                  <div className={styles.detailActions}>
                    <Button
                      variant="secondary"
                      onClick={() => {
                        setPromptToEdit(selectedPrompt);
                        setShowPromptModal(true);
                      }}
                    >
                      Edit
                    </Button>
                    <Button variant="ghost" onClick={() => setShowDeleteConfirm(true)}>
                      Delete
                    </Button>
                  </div>
                </div>
              ) : (
                <div className={styles.emptyState}>
                  Select a prompt to view details, or create a new prompt.
                </div>
              )}
            </div>
          </section>
        </div>
      </div>

      <Modal
        open={showPromptModal}
        title={promptToEdit ? "Edit prompt" : "Create new prompt"}
        onClose={() => {
          setShowPromptModal(false);
          setPromptToEdit(null);
        }}
      >
        <PromptForm
          initialPrompt={promptToEdit ?? undefined}
          collections={collections}
          submitLabel={promptToEdit ? "Save changes" : "Create prompt"}
          onSubmit={handlePromptSave}
          onCancel={() => {
            setShowPromptModal(false);
            setPromptToEdit(null);
          }}
        />
      </Modal>

      <Modal
        open={showCollectionModal}
        title="Create collection"
        onClose={() => setShowCollectionModal(false)}
      >
        <CollectionForm
          onSubmit={async (collection) => {
            setShowCollectionModal(false);
            try {
              await api.createCollection(collection);
              await loadCollections();
            } catch (err) {
              setError((err as Error).message || "Unable to create collection");
            }
          }}
          onCancel={() => setShowCollectionModal(false)}
        />
      </Modal>

      <Modal
        open={showDeleteConfirm}
        title="Confirm delete"
        onClose={() => setShowDeleteConfirm(false)}
        footer={
          <>
            <Button variant="secondary" onClick={() => setShowDeleteConfirm(false)}>
              Cancel
            </Button>
            <Button variant="primary" onClick={handleDeletePrompt}>
              Delete prompt
            </Button>
          </>
        }
      >
        <p>Are you sure you want to delete this prompt? This action cannot be undone.</p>
      </Modal>
    </Layout>
  );
}

export default App;