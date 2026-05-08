import styles from "./Layout.module.css";

export default function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.brand}>
        <span className={styles.logo}>10X</span>
        <span className={styles.title}>Engineer UI</span>
      </div>
      <nav className={styles.nav}>
        <a href="#">Dashboard</a>
        <a href="#">Projects</a>
        <a href="#">Teams</a>
      </nav>
    </header>
  );
}