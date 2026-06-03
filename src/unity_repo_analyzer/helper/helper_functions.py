
def patch_for_groq():
    # =====================================================================
    # EMERGENCY MONKEY-PATCH: Fixes CrewAI Bug injecting 'cache_breakpoint' into Groq
    # =====================================================================
    try:
        import crewai.llms.cache as _crewai_cache
        # Replaces the internal flag injector function with a safe pass-through lambda
        _crewai_cache.mark_cache_breakpoint = lambda msg: msg
        print("[PATCH] Successfully bypassed CrewAI cache_breakpoint injector for Groq.")
    except Exception as patch_error:
        print(f"[PATCH WARNING] Failed to apply Groq compatibility patch: {patch_error}")
    # =====================================================================