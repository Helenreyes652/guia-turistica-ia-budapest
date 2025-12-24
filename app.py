import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from PIL import Image
from io import BytesIO

# Configuración de la página
st.set_page_config(
    page_title="🚩 Tu Guía Personal en Budapest",
    page_icon="🚩",
    layout="wide"
)

# Título de la aplicación
st.title("🚩 Tu Guía Personal en Budapest")
st.markdown("### Descubre monumentos y museos con tu guía turística con IA")

# Sidebar para configuración
with st.sidebar:
    st.header("⚙️ Configuración")
    api_key = st.text_input(
        "API Key de Google Gemini",
        type="password",
        help="Introduce tu API Key de Google AI Studio"
    )
    
    if api_key:
        st.success("✅ API Key configurada")
    else:
        st.warning("⚠️ Necesitas configurar tu API Key para usar la aplicación")
    
    st.markdown("---")
    st.markdown("""
    **¿Cómo usar esta app?**
    1. Introduce tu API Key de Gemini
    2. Toma o sube una foto del monumento o sala del museo
    3. La IA identificará el lugar y te dará información
    4. Escucha la explicación en audio
    """)
    
    st.markdown("---")
    st.markdown("""
    **¿Cómo obtener tu API Key?**
    1. Ve a [Google AI Studio](https://aistudio.google.com/)
    2. Crea una API Key gratuita
    3. Cópiala y pégala aquí
    """)

# Área principal
if api_key:
    # Configurar la API de Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro-vision')
    
    # Input de imagen
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📸 Captura o sube una imagen")
        
        # Opción para subir imagen
        uploaded_file = st.file_uploader(
            "Sube una imagen del lugar",
            type=["jpg", "jpeg", "png"]
        )
        
        # Opción para tomar foto con cámara
        camera_photo = st.camera_input("O toma una foto con tu cámara")
        
        # Determinar qué imagen usar
        img_file = camera_photo if camera_photo else uploaded_file
        
        if img_file:
            # Mostrar la imagen
            image = Image.open(img_file)
            st.image(image, caption="Imagen capturada", use_container_width=True)
            
            # Botón para analizar
            if st.button("🔍 Analizar lugar y generar guía", type="primary"):
                with st.spinner("Analizando la imagen y generando guía turística..."):
                    try:
                        # Prompt para la IA
                        prompt = """
                        Eres un guía turístico experto en Budapest y Hungría. 
                        
                        Analiza esta imagen e identifica:
                        1. ¿Qué lugar, monumento o sala de museo es?
                        2. ¿Dónde se encuentra exactamente?
                        
                        Luego proporciona una explicación fascinante como guía turístico en español que incluya:
                        - Historia del lugar (2-3 minutos de lectura)
                        - Datos curiosos y anécdotas interesantes
                        - Detalles arquitectónicos o artísticos destacables
                        - Importancia cultural e histórica
                        - Consejos para los visitantes
                        
                        Usa un tono ameno, educativo y entusiasta. Divide la información en secciones claras.
                        
                        Si no puedes identificar el lugar específicamente, da información general sobre el tipo de arquitectura o arte que ves.
                        """
                        
                        # Generar contenido con Gemini
                        response = model.generate_content([prompt, image])
                        descripcion = response.text
                        
                        # Mostrar la descripción
                        st.success("✅ Análisis completado")
                        st.markdown("### 📖 Información del lugar")
                        st.markdown(descripcion)
                        
                        # Generar audio
                        with st.spinner("Generando audio en español..."):
                            tts = gTTS(descripcion, lang='es')
                            audio_fp = BytesIO()
                            tts.write_to_fp(audio_fp)
                            audio_fp.seek(0)                            # Reproducir audio
                            st.markdown("### 🔊 Escucha la explicación")
                            st.audio(audio_fp, format='audio/mp3')                            
                            st.info("""
                            💡 **Consejo:** Cuando llegues al siguiente punto de interés, 
                            vuelve a tomar una foto para obtener nueva información.
                            """)
                            
                    except Exception as e:
                        st.error(f"❌ Error al procesar la imagen: {str(e)}")
                        st.info("Verifica que tu API Key sea válida y que tengas conexión a internet.")
    
    with col2:
        st.subheader("ℹ️ Información")
        st.info("""
        **Esta aplicación puede identificar:**
        
        🏛️ Monumentos históricos
        
        🏰 Castillos y palacios
        
        ⛪ Iglesias y catedrales
        
        🎨 Obras de arte en museos
        
        🏛️ Salas de museos
        
        🌉 Puentes y edificios emblemáticos
        """)
        
        st.success("""
        **Funciona en cualquier lugar del mundo**, 
        aunque está optimizada para Budapest.
        """)

else:
    st.info("👈 Por favor, configura tu API Key en la barra lateral para comenzar.")
    
    # Mostrar información de ejemplo
    st.markdown("### Características de la aplicación")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 📸 Reconocimiento visual
        Usa la cámara de tu dispositivo o sube fotos para identificar lugares
        """)
    
    with col2:
        st.markdown("""
        #### 🤖 IA avanzada
        Powered by Google Gemini para identificación precisa
        """)
    
    with col3:
        st.markdown("""
        #### 🔊 Guía en audio
        Escucha las explicaciones mientras exploras
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Hecho con ❤️ usando Google Gemini AI y Streamlit</p>
    <p>🇭🇺 Perfecto para explorar Budapest y otros destinos turísticos</p>
</div>
""", unsafe_allow_html=True)
