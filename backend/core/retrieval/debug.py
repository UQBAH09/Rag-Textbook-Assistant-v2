def print_results(results, max_chars=300):
    for i, r in enumerate(results, 1):
        node = r.node
        meta = node.metadata or {}

        print(f"\n#{i} | score={r.score:.4f}")
        print(
            f"Book={meta.get('book_id')} | "
            f"Chapter={meta.get('chapter_number')} ({meta.get('chapter_name')}) | "
            f"Section={meta.get('section_number')} ({meta.get('section_name')}) | "
            f"Pages={meta.get('page_start')}-{meta.get('page_end')}"
        )

        preview = node.get_content()[:max_chars].replace("\n", " ")
        print(preview, "...")
