def patch():
    """
    Applies emergency monkey-patches to address critical compatibility issues.
    This function is called at the very start of the application to ensure all
    patches are in place before any imports that might be affected.
    """
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