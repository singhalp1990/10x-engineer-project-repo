import styles from "./Layout.module.css";

const collections = [
  { title: "Overview", id: "overview" },
  { title: "Inventory", id: "inventory" },
  { title: "Orders", id: "orders" },
  { title: "Reports", id: "reports" }
];

export default function Sidebar() {
  return (
    <aside className={styles.sidebar}>
      <h2 className={styles.sidebarTitle}>Collections</h2>
      <ul className={styles.sidebarList}>
        {collections.map((item) => (
          <li key={item.id} className={styles.sidebarItem}>
            <a href={`#${item.id}`}>{item.title}</a>
          </li>
        ))}
      </ul>
    </aside>
  );
}