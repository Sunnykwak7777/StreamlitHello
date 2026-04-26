import streamlit as st
import streamlit.components.v1 as components


def load_keyboard_class():
    st.markdown(
        """
        <style>
        .kbdx {
            background-color: #eee;
            border-radius: 3px;
            border: 1px solid #b4b4b4;
            box-shadow: 0 1px 1px rgba(0,0,0,.2), 0 2px 0 0 rgba(255,255,255,.7) inset;
            color: #333;
            display: inline-block;
            font-size: .85em;
            font-weight: 700;
            line-height: 1;
            padding: 2px 4px;
            white-space: nowrap;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def keyboard_to_url(key=None, key_code=None, url=""):
    if key:
        js = f"""
        <script>
        document.addEventListener('keydown', function(e) {{
            if (e.key === '{key}' && !e.ctrlKey && !e.metaKey && !e.altKey
                && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {{
                window.open('{url}', '_blank');
            }}
        }});
        </script>
        """
    elif key_code:
        js = f"""
        <script>
        document.addEventListener('keydown', function(e) {{
            if (e.keyCode === {key_code} && !e.ctrlKey && !e.metaKey && !e.altKey
                && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {{
                window.open('{url}', '_blank');
            }}
        }});
        </script>
        """
    else:
        return
    components.html(js, height=0)
