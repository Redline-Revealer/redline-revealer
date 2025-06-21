import os
import json
import logging
from typing import Optional, Dict, Any
from azure.maps.render import MapsRenderClient
from azure.identity import DefaultAzureCredential
import streamlit as st

class AzureMapRenderer:
    """Complete Azure Maps renderer with error handling"""
    
    def __init__(self):
        try:
            self.key = st.secrets[""]
            self.ready = True
            self._setup_styles()
        except Exception as e:
            logging.error(f"Azure init failed: {str(e)}")
            self.ready = False

    def _setup_styles(self):
        self.holc_style = {
            'A': {'fill': '#00FF00', 'stroke': '#000000'},
            'B': {'fill': '#FFFF00', 'stroke': '#000000'},
            'C': {'fill': '#FFA500', 'stroke': '#000000'},
            'D': {'fill': '#FF0000', 'stroke': '#000000'},
            'default': {'fill': '#CCCCCC', 'stroke': '#000000'}
        }

    def render(self, geojson_data: Dict[str, Any]) -> Optional[str]:
        """Generate Azure Maps URL with overlays"""
        if not self.ready:
            return None

        try:
            client = MapsRenderClient(
                credential=DefaultAzureCredential(),
                subscription_key=self.key
            )
            
            # Style each feature
            features = []
            for feature in geojson_data['features']:
                grade = feature['properties'].get('grade', '').upper()
                style = self.holc_style.get(grade, self.holc_style['default'])
                
                styled_feature = {
                    **feature,
                    'properties': {
                        **feature['properties'],
                        '_azure_style': style
                    }
                }
                features.append(styled_feature)

            response = client.render_geojson({
                "type": "FeatureCollection",
                "features": features
            }, style={
                'fillColor': ['get', ['get', '_azure_style'], ['get', 'fill']],
                'strokeColor': ['get', ['get', '_azure_style'], ['get', 'stroke']],
                'fillOpacity': 0.7
            })
            
            return response.map_url
        except Exception as e:
            logging.error(f"Rendering failed: {str(e)}")
            return None