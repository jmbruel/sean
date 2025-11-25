---
title: Global Map
date: 2025-11-25

type: landing

sections:
  - block: hero
    content:
      title: SEAN Team Around the World
      text: Our team spans across multiple countries in Europe and beyond. Explore the interactive map below to see where our members are based.
    design:
      background:
        gradient_end: '#1976d2'
        gradient_start: '#004ba0'
        text_color_light: true
      
  - block: markdown
    content:
      title: Team Locations Map
      subtitle: ''
      text: |
        <div id="map-container" style="width: 100%; height: 600px; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
          <!-- Map will be rendered here -->
        </div>
        
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

        <script>
          // Initialize map centered on Europe
          const map = L.map('map-container').setView([54.5260, 15.2551], 4);
          
          // Add OpenStreetMap tile layer
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
          }).addTo(map);
          
          // Team members data
          const teamMembers = [
            { name: 'Jean-Michel Bruel', country: 'France', lat: 43.5628, lng: 1.4545, org: 'University of Toulouse' },
            { name: 'Sébastien Mosser', country: 'Canada', lat: 43.2557, lng: -79.8711, org: 'McMaster University' },
            { name: 'Ana Moreira', country: 'Portugal', lat: 38.6597, lng: -9.0156, org: 'NOVA University of Lisbon' },
            { name: 'Antonia Bertolina', country: 'Italy', lat: 42.3631, lng: 13.3972, org: 'Gran Sasso Science Institute' },
            { name: 'Bertrand Meyer', country: 'Switzerland', lat: 47.3769, lng: 8.5472, org: 'Constructor Institute' },
            { name: 'Gilles Perrouin', country: 'Belgium', lat: 50.4501, lng: 4.4699, org: 'University of Namur' },
            { name: 'Steffen Zschaler', country: 'United Kingdom', lat: 51.5074, lng: -0.1278, org: 'Kings College London' },
            { name: 'Timo Kehrer', country: 'Switzerland', lat: 46.9479, lng: 7.4474, org: 'University of Bern' }
          ];
          
          // Add markers for each team member
          teamMembers.forEach(member => {
            const marker = L.circleMarker([member.lat, member.lng], {
              radius: 8,
              fillColor: '#1976d2',
              color: '#004ba0',
              weight: 2,
              opacity: 0.8,
              fillOpacity: 0.7
            }).addTo(map);
            
            marker.bindPopup(`
              <div style="font-weight: bold;">${member.name}</div>
              <div style="font-size: 0.9em; color: #666;">${member.country}</div>
              <div style="font-size: 0.85em; color: #999;">${member.org}</div>
            `);
          });
          
          // Highlight countries with team members
          const countryCodes = {
            'FR': 'France',
            'CA': 'Canada',
            'PT': 'Portugal',
            'IT': 'Italy',
            'CH': 'Switzerland',
            'BE': 'Belgium',
            'GB': 'United Kingdom'
          };
          
          // Add a legend
          const legend = L.control({ position: 'bottomright' });
          legend.onAdd = function() {
            const div = L.DomUtil.create('div', 'info');
            div.style.backgroundColor = 'white';
            div.style.padding = '10px';
            div.style.borderRadius = '4px';
            div.style.boxShadow = '0 0 15px rgba(0,0,0,0.2)';
            div.innerHTML = `
              <div style="font-weight: bold; margin-bottom: 8px;">Team Locations</div>
              <div style="font-size: 0.9em;">
                🔵 Team Member Location
              </div>
              <div style="font-size: 0.85em; color: #666; margin-top: 8px;">
                Click markers for details
              </div>
            `;
            return div;
          };
          legend.addTo(map);
        </script>
        
        ## Team Members by Country
        
        | Country | Members |
        |---------|---------|
        | 🇫🇷 France | Jean-Michel Bruel |
        | 🇨🇦 Canada | Sébastien Mosser |
        | 🇵🇹 Portugal | Ana Moreira |
        | 🇮🇹 Italy | Antonia Bertolina |
        | 🇨🇭 Switzerland | Bertrand Meyer, Timo Kehrer |
        | 🇧🇪 Belgium | Gilles Perrouin |
        | 🇬🇧 United Kingdom | Steffen Zschaler |

---
