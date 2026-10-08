document.addEventListener("DOMContentLoaded", function() {
  fetch('/feeds/posts/default?alt=json&max-results=10')
    .then(function(response) { return response.json(); })
    .then(function(data) {
      let container = document.getElementById('recent-posts-resume-list');
      let entries = data.feed.entry || [];
      let html = '';

      html += '<h5 style="color: inherit; font-size: 16px; margin: 20px 0 10px 0;">RECENT POSTS</h5>';
      
      container.innerHTML = html;

      for (let i = 0; i < entries.length; i++) {
        let entry = entries[i];
        let title = entry.title.$t;
        let link = '#';

        for (let j = 0; j < entry.link.length; j++) {
          if (entry.link[j].rel === 'alternate') {
            link = entry.link[j].href;
            break;
          }
        }

        let snippet = '';
        let contentHtml = '';
        if (entry.summary) {
          snippet = entry.summary.$t;
        } else if (entry.content) {
          contentHtml = entry.content.$t;
          var tempDiv = document.createElement('div');
          tempDiv.innerHTML = contentHtml;
          snippet = tempDiv.textContent || tempDiv.innerText || '';
          if (snippet.length > 160) {
            snippet = snippet.substring(0, 160) + '...';
          }
        }

        let thumbUrl = '';
        if (entry.media$thumbnail && entry.media$thumbnail.url) {
          thumbUrl = entry.media$thumbnail.url;
        } else if (contentHtml) {
          var imgMatch = contentHtml.match(/<img[^>]+src="([^">]+)"/);
          if (imgMatch) {
            thumbUrl = imgMatch[1];
          }
        }
      
      // 1. Crear el elemento <article> principal
        let article = document.createElement('article');
        article.className = 'post';
        article.setAttribute('role', 'article');
        article.style.cssText = 'background: #fff; padding: 15px; margin-bottom: 16px; box-sizing: border-box; width: 100%; word-break: break-word;';

        // 2. Comentario: Ad before post
        article.appendChild(document.createComment(' Ad before post '));

        // 3. Contenedor de anuncios (Antes)
        let adBefore = document.createElement('div');
        adBefore.className = 'ads-antes-body';
        adBefore.style.cssText = 'margin: 15px 0; text-align: center; width: 100%; box-sizing: border-box;';

        let scriptOpt1 = document.createElement('script');
        scriptOpt1.textContent = 'atOptions = {"key": "965f52969e90286ccd9b08a873f54c8a", "format": "iframe", "height": 250, "width": 300, "params": {}};';
        adBefore.appendChild(scriptOpt1);

        let scriptInvoke1 = document.createElement('script');
        scriptInvoke1.src = 'https://www.highrevenueformat.com/965f52969e90286ccd9b08a873f54c8a/invoke.js';
        adBefore.appendChild(scriptInvoke1);

        let ins1 = document.createElement('ins');
        ins1.className = 'adsbygoogle';
        ins1.setAttribute('data-ad-client', 'ca-pub-2334449220276386');
        ins1.setAttribute('data-ad-format', 'auto');
        ins1.setAttribute('data-ad-slot', '9525388880');
        ins1.setAttribute('data-full-width-responsive', 'true');
        ins1.style.display = 'block';
        adBefore.appendChild(ins1);

        article.appendChild(adBefore);

        // 4. Título del post (<h3>) con su enlace (<a>)
        let h3 = document.createElement('h3');
        h3.className = 'post-title';
        h3.style.cssText = 'font: bold 20px Roboto, sans-serif; margin: 0 0 8px 0; float: none; width: 100%; clear: both; word-break: break-word;';

        let titleLink = document.createElement('a');
        titleLink.href = link;
        titleLink.style.cssText = 'color: #212121; text-decoration: none;';
        titleLink.textContent = title;
        h3.appendChild(titleLink);
        article.appendChild(h3);

        // 5. Miniatura (si thumbUrl existe)
        if (thumbUrl) {
            let thumbDiv = document.createElement('div');
            thumbDiv.className = 'snippet-thumbnail';
            thumbDiv.style.cssText = 'float: left; margin: 0 15px 10px 0; max-height: 128px; max-width: 128px;';

            let img = document.createElement('img');
            img.src = thumbUrl;
            img.style.cssText = 'max-width: 100%; height: auto; display: block;';
            
            thumbDiv.appendChild(img);
            article.appendChild(thumbDiv);
        }

        // 6. Snippet del post
        let snippetDiv = document.createElement('div');
        snippetDiv.className = 'post-snippet';
        snippetDiv.style.cssText = 'color: #757575; font-size: 15px; line-height: 1.6em; margin: 10px 0; clear: none; word-break: break-word;';
        snippetDiv.textContent = snippet;
        article.appendChild(snippetDiv);

        // 7. Enlace "READ MORE"
        let readMoreWrapper = document.createElement('div');
        readMoreWrapper.style.cssText = 'clear: both; margin-bottom: 10px;';

        let readMoreLink = document.createElement('a');
        readMoreLink.href = link;
        readMoreLink.style.cssText = 'color: #2196f3; text-decoration: none; font-weight: bold;';
        readMoreLink.textContent = 'READ MORE';

        readMoreWrapper.appendChild(readMoreLink);
        article.appendChild(readMoreWrapper);

        // 8. Div limpiador (clear)
        let clearDiv1 = document.createElement('div');
        clearDiv1.style.cssText = 'clear: both;';
        article.appendChild(clearDiv1);

        // 9. Comentario: Ad after post
        article.appendChild(document.createComment(' Ad after post '));

        // 10. Contenedor de anuncios (Después)
        let adAfter = document.createElement('div');
        adAfter.className = 'ads-despues-body';
        adAfter.style.cssText = 'margin: 15px 0; text-align: center; width: 100%; box-sizing: border-box;';

        let scriptOpt2 = document.createElement('script');
        scriptOpt2.textContent = 'atOptions = {"key": "965f52969e90286ccd9b08a873f54c8a", "format": "iframe", "height": 250, "width": 300, "params": {}};';
        adAfter.appendChild(scriptOpt2);

        let scriptInvoke2 = document.createElement('script');
        scriptInvoke2.src = 'https://www.highrevenueformat.com/965f52969e90286ccd9b08a873f54c8a/invoke.js';
        adAfter.appendChild(scriptInvoke2);

        let ins2 = document.createElement('ins');
        ins2.className = 'adsbygoogle';
        ins2.setAttribute('data-ad-client', 'ca-pub-2334449220276386');
        ins2.setAttribute('data-ad-format', 'auto');
        ins2.setAttribute('data-ad-slot', '9525388880');
        ins2.setAttribute('data-full-width-responsive', 'true');
        ins2.style.display = 'block';
        adAfter.appendChild(ins2);

        article.appendChild(adAfter);

        // 11. Finalmente, agregamos todo el artículo armado al contenedor principal
        container.appendChild(article);
      }

      // Inyectar el HTML completo en el contenedor
      //container.innerHTML = html;

      // --- INICIALIZAR ADSENSE ---
      let insElements = container.querySelectorAll('.adsbygoogle');
      for (let k = 0; k < insElements.length; k++) {
        try {
          (window.adsbygoogle = window.adsbygoogle || []).push({});
        } catch (e) {
          console.error(e);
        }
      }
    }).catch(function(err) {
      console.error('Error al cargar los posts recientes:', err);
    });
});
