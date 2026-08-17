from t_search.stage1 import canonical_block, compare_blocks, project_all_views
from t_search.stage1_missing_views import enumerate_latent_edge_completions, reconstruct_missing_views


def without_views(*event_ids: str):
    removed = set(event_ids)
    return tuple(view for view in project_all_views(canonical_block()) if view.event_id not in removed)


def main() -> None:
    original = canonical_block()

    print("=== Case A: remove V_d ===")
    views = without_views("d")
    strict = reconstruct_missing_views(views, policy="strict")
    latent = reconstruct_missing_views(views, policy="latent")
    print("strict events:", sorted(strict.block.events))
    print("strict edges:", sorted(strict.block.direct_edges))
    print("strict dangling:", sorted(strict.dangling_references))
    print("latent events:", sorted(latent.block.events))
    print("latent edges:", sorted(latent.block.direct_edges))
    print("latent IDs:", sorted(latent.latent_events))
    print("comparison:", compare_blocks(original, latent.block))
    print("candidate completions:", len(enumerate_latent_edge_completions(latent)))

    print("\n=== Case B: remove V_b and V_d ===")
    views = without_views("b", "d")
    latent = reconstruct_missing_views(views, policy="latent")
    candidates = enumerate_latent_edge_completions(latent)
    print("evidence events:", sorted(latent.block.events))
    print("evidence edges:", sorted(latent.block.direct_edges))
    print("latent IDs:", sorted(latent.latent_events))
    print("candidate completions:", len(candidates))
    print("original among candidates:", original in candidates)
    for index, candidate in enumerate(candidates, start=1):
        print(f"candidate {index}:", sorted(candidate.direct_edges))

    print("\n=== Case C: remove V_d and V_e ===")
    views = without_views("d", "e")
    latent = reconstruct_missing_views(views, policy="latent")
    print("events:", sorted(latent.block.events))
    print("edges:", sorted(latent.block.direct_edges))
    print("latent IDs:", sorted(latent.latent_events))
    print("event e recovered:", "e" in latent.block.events)


if __name__ == "__main__":
    main()
