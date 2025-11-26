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
          // Initialize map centered on the Atlantic Ocean between Canada and Europe
          const map = L.map('map-container').setView([50, -25], 3);
          
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
          
          // Country code mapping for easier lookup
          const countryData = {
            'France': { code: 'FR', color: '#FF6B6B' },
            'Canada': { code: 'CA', color: '#4ECDC4' },
            'Portugal': { code: 'PT', color: '#45B7D1' },
            'Italy': { code: 'IT', color: '#96CEB4' },
            'Switzerland': { code: 'CH', color: '#FFEAA7' },
            'Belgium': { code: 'BE', color: '#DDA0DD' },
            'United Kingdom': { code: 'GB', color: '#FFB6C1' }
          };
          
          // Create a set of unique countries with team members
          const activeCountries = new Set(teamMembers.map(m => m.country));
          
          // Add GeoJSON layer with country highlighting (robust matching)
          fetch('countries.geo.json')
            .then(response => response.json())
            .then(data => {
              const highlightColor = '#4ECDC4';

              const normalize = s => (s || '')
                .toString()
                .toLowerCase()
                .replace(/\(.*?\)/g, '')
                .replace(/[^a-z0-9 ]+/g, ' ')
                .replace(/\s+/g, ' ')
                .trim();

              const alias = {
                'uk': 'united kingdom',
                'united kingdom of great britain and northern ireland': 'united kingdom',
                'ivory coast': "cote d'ivoire",
                'russia': 'russian federation'
              };

              const activeList = Array.from(activeCountries);
              const activeNorms = activeList.reduce((acc, name) => {
                acc[normalize(name)] = name;
                return acc;
              }, {});

              const matchedGeoNames = new Set();

              function findTeamCountry(geoName) {
                if (!geoName) return null;
                const n = normalize(geoName);
                if (activeNorms[n]) return activeNorms[n];
                if (alias[n] && activeNorms[alias[n]]) return activeNorms[alias[n]];
                for (const k of Object.keys(activeNorms)) {
                  if (n === k) return activeNorms[k];
                  if (n.indexOf(k) !== -1) return activeNorms[k];
                  if (k.indexOf(n) !== -1) return activeNorms[k];
                }
                return null;
              }

              L.geoJSON(data, {
                style(feature) {
                  const props = feature.properties || {};
                  const geoName = props.name || props.ADMIN || props.NAME || '';
                  const teamCountry = findTeamCountry(geoName);
                  if (teamCountry) {
                    matchedGeoNames.add(geoName);
                    return {
                      fillColor: highlightColor,
                      weight: 2,
                      opacity: 0.9,
                      color: '#2a7f7e',
                      fillOpacity: 0.55
                    };
                  }
                  return {
                    fillColor: '#f0f0f0',
                    weight: 0.5,
                    opacity: 0.3,
                    color: '#ddd',
                    fillOpacity: 0.06
                  };
                },
                onEachFeature(feature, layer) {
                  const props = feature.properties || {};
                  const geoName = props.name || props.ADMIN || props.NAME || '';
                  const teamCountry = findTeamCountry(geoName);
                  if (teamCountry) {
                    const members = teamMembers.filter(m => m.country === teamCountry);
                    const membersList = members.map(m => `<li>${m.name}</li>`).join('');
                    layer.bindPopup(`
                      <div style="font-weight: bold; font-size: 1.1em;">${teamCountry}</div>
                      <div style="margin-top: 8px;">
                        <strong>Team Members:</strong>
                        <ul style="margin: 4px 0; padding-left: 20px;">${membersList}</ul>
                      </div>
                    `);
                    layer.on('mouseover', () => layer.setStyle({ weight: 3 }));
                    layer.on('mouseout', () => layer.setStyle({ weight: 2 }));
                  }
                }
              }).addTo(map);

              // Debug: log what matched and what didn't
              setTimeout(() => {
                console.info('Active countries:', activeList);
                console.info('Matched Geo feature names (sample):', Array.from(matchedGeoNames).slice(0,20));
              }, 300);
            })
            .catch(err => console.error('Error loading GeoJSON:', err));
          
          // Add markers for each team member
          teamMembers.forEach(member => {
            const marker = L.circleMarker([member.lat, member.lng], {
              radius: 8,
              fillColor: '#1976d2',
              color: '#004ba0',
              weight: 2,
              opacity: 0.9,
              fillOpacity: 0.8
            }).addTo(map);
            
            marker.bindPopup(`
              <div style="font-weight: bold;">${member.name}</div>
              <div style="font-size: 0.9em; color: #666;">${member.country}</div>
              <div style="font-size: 0.85em; color: #999;">${member.org}</div>
            `);
          });
          
          // Add a legend
          const legend = L.control({ position: 'bottomright' });
          legend.onAdd = function() {
            const div = L.DomUtil.create('div', 'info');
            div.style.backgroundColor = 'white';
            div.style.padding = '10px';
            div.style.borderRadius = '4px';
            div.style.boxShadow = '0 0 15px rgba(0,0,0,0.2)';
            div.innerHTML = `
              <div style="font-weight: bold; margin-bottom: 8px;">Legend</div>
              <div style="font-size: 0.9em; margin-bottom: 6px;">
                <span style="display: inline-block; width: 12px; height: 12px; background-color: #1976d2; border-radius: 50%; margin-right: 6px;"></span> Team Member
              </div>
              <div style="font-size: 0.9em; margin-bottom: 6px;">
                <span style="display: inline-block; width: 12px; height: 12px; background-color: #FF6B6B; opacity: 0.4; margin-right: 6px;"></span> Country with Team
              </div>
              <div style="font-size: 0.85em; color: #666; margin-top: 8px;">
                Click markers or countries for details
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
