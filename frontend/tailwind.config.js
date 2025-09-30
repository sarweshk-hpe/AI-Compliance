/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // HPE Brand Color
        'hpe-brand': '#01a982',
        
        // HPE Core Palette
        'hpe-core': {
          purple: '#7630EA',
          teal: '#00e8cf',
          blue: '#00739d',
          red: '#c54e4b',
          orange: '#FF8300',
          yellow: '#fec901',
        },
        
        // HPE Light Palette
        'hpe-light': {
          green: '#17eba0',
          purple: '#f740ff',
          teal: '#82fff2',
          blue: '#00c8ff',
          red: '#fc6161',
          orange: '#ffbc44',
          yellow: '#ffeb59',
        },
        
        // HPE Dark Palette
        'hpe-dark': {
          green: '#008567',
          purple: '#6633bc',
          teal: '#117b82',
          blue: '#00739d',
          red: '#a2423d',
          orange: '#9b6310',
          yellow: '#8d741c',
        },
        
        // HPE Background Colors
        'hpe-bg': {
          light: {
            background: '#ffffff',
            'background-back': '#f7f7f7',
            'background-front': '#ffffff',
            'background-contrast': 'rgba(0, 0, 0, 0.04)',
          },
          dark: {
            background: '#1c1c1c',
            'background-back': '#1c1c1c',
            'background-front': '#222222',
            'background-contrast': 'rgba(255, 255, 255, 0.12)',
          },
        },
        
        // HPE Border Colors
        'hpe-border': {
          light: {
            border: 'rgba(0, 0, 0, 0.36)',
            'border-strong': 'rgba(0, 0, 0, 0.72)',
            'border-weak': 'rgba(0, 0, 0, 0.12)',
          },
          dark: {
            border: 'rgba(255, 255, 255, 0.36)',
            'border-strong': 'rgba(255, 255, 255, 0.72)',
            'border-weak': 'rgba(255, 255, 255, 0.12)',
          },
        },
        
        // HPE Input Colors
        'hpe-input': {
          light: {
            'validation-critical': '#ffecec',
            'validation-ok': '#e3fdf4',
            'validation-warning': '#fff3dd',
          },
          dark: {
            'validation-critical': '#552120',
            'validation-ok': '#1b5245',
            'validation-warning': '#3c361e',
          },
        },
        
        // HPE Text Colors
        'hpe-text': {
          light: {
            text: '#555555',
            'text-strong': '#2e2e2e',
            'text-weak': '#676767',
            'text-xweak': '#676767',
          },
          dark: {
            text: '#ffffff',
            'text-strong': '#ffffff',
            'text-weak': 'rgba(255, 255, 255, 0.61)',
            'text-xweak': 'rgba(255, 255, 255, 0.61)',
          },
        },
        
        // HPE Status Colors
        'hpe-status': {
          light: {
            critical: '#ec3331',
            warning: '#d36d00',
            ok: '#009a71',
            unknown: '#757575',
          },
          dark: {
            critical: '#fc5a5a',
            warning: '#d36d00',
            ok: '#1ed8ae',
            unknown: '#8c8c8c',
          },
        },
        
        // HPE Focus Color
        'hpe-focus': '#004233',
        
        // HPE Elevation
        'hpe-elevation': {
          light: {
            small: '0 2px 4px rgba(0, 0, 0, 0.12)',
            medium: '0px 6px 12px 0px rgba(0, 0, 0, 0.12)',
            large: '0px 12px 24px 0px rgba(0, 0, 0, 0.24)',
          },
          dark: {
            small: '0 2px 4px rgba(0, 0, 0, 0.24)',
            medium: '0px 6px 12px 0px rgba(0, 0, 0, 0.36)',
            large: '0px 12px 24px 0px rgba(0, 0, 0, 0.48)',
          },
        },
        
        // HPE Overlay Color
        'hpe-overlay': 'background-screenOverlay',
        
        // HPE Graph Colors
        'hpe-graph': {
          light: {
            0: '#3c3aa1',
            1: '#b0840d',
            2: '#a95589',
            3: '#2053d9',
            4: '#a78972',
            5: '#7022ec',
            6: '#38819c',
            7: '#470d69',
          },
          dark: {
            0: '#7372cf',
            1: '#bd9d48',
            2: '#c0649a',
            3: '#5c91e5',
            4: '#a68a74',
            5: '#b889ff',
            6: '#4d8da8',
            7: '#855aaa',
          },
        },
      },
      boxShadow: {
        'hpe-elevation-small-light': '0 2px 4px rgba(0, 0, 0, 0.12)',
        'hpe-elevation-medium-light': '0px 6px 12px 0px rgba(0, 0, 0, 0.12)',
        'hpe-elevation-large-light': '0px 12px 24px 0px rgba(0, 0, 0, 0.24)',
        'hpe-elevation-small-dark': '0 2px 4px rgba(0, 0, 0, 0.24)',
        'hpe-elevation-medium-dark': '0px 6px 12px 0px rgba(0, 0, 0, 0.36)',
        'hpe-elevation-large-dark': '0px 12px 24px 0px rgba(0, 0, 0, 0.48)',
      },
    },
  },
  plugins: [],
}
