import streamlit as st

# Define the JS loader
daisy_loader = """
<script>
    (function() {
        // 1. Load DaisyUI CSS
        if (!document.getElementById('daisy-css')) {
            const link = document.createElement('link');
            link.id = 'daisy-css';
            link.rel = 'stylesheet';
            link.type = 'text/css';
            link.href = 'https://cdn.jsdelivr.net/npm/daisyui@5/daisyui.min.css';
            document.head.appendChild(link);
        }

        // 2. Load Tailwind JS (Optional if you use the standalone script)
        if (!document.getElementById('tailwind-js')) {
            const script = document.createElement('script');
            script.id = 'tailwind-js';
            script.src = 'https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4';
            document.head.appendChild(script);
        }
    })();
</script>
"""

# Inject the loader once
st.html(daisy_loader, unsafe_allow_javascript=True)

# Now you can use DaisyUI classes directly in st.html
st.html("""
    <div class="p-10">
        <button class="btn btn-primary">DaisyUI v5 Button</button>
        <div class="badge badge-secondary mt-4">Tailwind v4 Powered</div>
    </div>
""")