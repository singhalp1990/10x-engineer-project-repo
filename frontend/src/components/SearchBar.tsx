import styles from "./SharedComponents.module.css";

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  onSearch?: () => void;
}

export default function SearchBar({ value, onChange, placeholder = "Search...", onSearch }: SearchBarProps) {
  return (
    <form
      className={styles.searchBar}
      onSubmit={(event) => {
        event.preventDefault();
        onSearch?.();
      }}
    >
      <label className={styles.srOnly} htmlFor="prompt-search">
        Search prompts
      </label>
      <input
        id="prompt-search"
        type="search"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        className={styles.searchInput}
      />
      <button type="submit" className={styles.searchButton}>
        Search
      </button>
    </form>
  );
}