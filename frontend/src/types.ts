export interface Prompt {
  id: string;
  title: string;
  description: string;
  example: string;
  tags: string[];
  collectionId?: string;
  createdAt: string;
}

export interface Collection {
  id: string;
  name: string;
  description?: string;
  promptCount: number;
}