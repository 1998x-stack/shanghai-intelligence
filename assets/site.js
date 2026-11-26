(() => {
  "use strict";
  const input = document.querySelector("#archive-search");
  const items = Array.from(document.querySelectorAll("#searchable-events .event-card"));
  const counter = document.querySelector("#search-result");
  if (!input || !counter) return;
  const refresh = () => {
    const query = input.value.trim().toLocaleLowerCase("zh-CN");
    let visible = 0;
    for (const card of items) {
      const matches = card.dataset.search.toLocaleLowerCase("zh-CN").includes(query);
      card.hidden = !matches;
      if (matches) visible += 1;
    }
    counter.textContent = query ? "找到 " + visible + " 条符合条件的事件" : "共 " + items.length + " 条已核验事件";
  };
  input.addEventListener("input", refresh);
  refresh();
})();
