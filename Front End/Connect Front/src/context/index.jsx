import React from "react";
import PropTypes from "prop-types";

export const MaterialTailwind = React.createContext(null);
MaterialTailwind.displayName = "MaterialTailwindContext";

export const navColors = {
  dark: "from-black to-black border-gray-200",
  green: "from-green2-500 to-green2-700",
  orange: "from-orange-400 to-orange-600",
  red: "from-red-400 to-red-600",
  pink: "from-pink-400 to-pink-600",
};

//Reads from Local Storage
let font = localStorage.getItem("font");
if (font === null) {
  localStorage.setItem("font", "Normal");
  font = "Normal";
}

let theme = localStorage.getItem("theme");
if (theme === null) {
  localStorage.setItem("theme", "light");
  theme = "light";
}


/**
 * Retrieves the font value stored in local storage.
 *
 * @return {string} The font value from local storage.
 */
export function getFont() {
  return font;
}

export function getTypography() {
  if(font === "OpenDyslexic") {
    return "font-OpenDyslexic";
  } 
  else {
    return "font-normal";
  }
}

export function getTypographybold() {
  if(font === "OpenDyslexic") {
    return "font-OpenDyslexicBold";
  }
  else {
    return "font-bold";
  }
}

export function getTheme() {
  return theme;
}

export function getBorderColor(color) {
  if (theme === "light") {
    switch (color) {
      case "dark":
        return "border-gray-500";
      case "green":
        return "border-green-500";
      case "orange":
        return "border-orange-500";
      case "red":
        return "border-red-500";
      case "pink":
        return "border-pink-500";
      case "background":
        return "border-white";
      case "background-cards":
        return "border-white";
      case "search-bar":
        return "border-black";
      default:
        return "border-white";
    }
  } else {
    switch (color) {
      case "dark":
        return "border-gray-100";
      
      case "green":
        return "border-green-500";
      case "orange":
        return "border-orange-500";
      case "red":
        return "border-red-500";
      case "pink":
        return "border-pink-500";
      case "background":
        return "border-gray-900";
      case "background-cards":
        return "border-gray-500";
      case "search-bar":
        return "border-gray-800";
      default:
        return "border-gray-100";
    }
  }
}

export function getBgColor(color) {
  const [controller, dispatch] = useMaterialTailwindController();
  const { theme } =
    controller;

  if (theme === "light") {
    switch (color) {
      case "dark":
        return "bg-gray-500";
      case "green":
        return "bg-green2-700";
      case "orange":
        return "bg-orange-500";
      case "red":
        return "bg-red-500";
      case "pink":
        return "bg-pink-300";
      case "purple":
        return "bg-purple-500";
      case "blue":
        return "bg-blue-500";
      case "yellow":
        return "bg-blue-300";
      case "background":
        return "bg-white";
      case "background-cards":
        return "bg-white";
      case "search-bar":
        return "bg-black";
      case "gray":
        return "bg-gray-200";
      default:
        return "bg-white";
    }
  } else {
    switch (color) {
      case "dark":
        return "bg-gray-800";
      case "green":
        return "bg-green2-700";
      case "orange":
        return "bg-orange-500";
      case "red":
        return "bg-red-500";
      case "pink":
        return "bg-pink-300";
      case "purple":
          return "bg-purple-500";
      case "blue":
          return "bg-blue-500";
      case "yellow":
          return "bg-blue-300";
      case "background":
        return "bg-black";
      case "background-cards":
        return "bg-gray-900";
      case "search-bar":
        return "bg-gray-800";
      case "gray":
        return "bg-gray-600";
      default:
        return "bg-gray-100";
    }
  }
}

export function getTextColor(color) {
  const [controller, dispatch] = useMaterialTailwindController();
  const { theme } =
    controller;

  if (theme === "light") {
    switch (color) {
      case "dark":
        return "text-black";
      case "white":
        return "text-white";
      case "white2":
        return "text-white";
      case "contrast":
        return "text-black";
      case "gray":
        return "text-gray-500";
      case "bgray":
        return "text-gray-800";
      case "green":
        return "text-green-500";
      case "orange":
        return "text-orange-500";
      case "red":
        return "text-red-500";
      case "pink":
        return "text-pink-500";
      case "text-gray-300":
        return "text-green-300";
      default:
        return "text-black-100";
    }
  } else {
    switch (color) {
      case "dark":
        return "text-white";
      case "white":
        return "text-gray-900";
      case "white2":
        return "text-white";
      case "white3":
        return "text-white";
      case "contrast":
        return "text-white";
      case "gray":
        return "text-gray-300";
      case "green":
        return "text-green-500";
      case "orange":
        return "text-orange-500";
      case "red":
        return "text-red-500";
      case "pink":
        return "text-pink-500";
      case "text-gray-300":
        return "text-green-300";
      default:
        return "text-white";
    } 
  }
}


export function reducer(state, action) {
  switch (action.type) {
    case "OPEN_SIDENAV": {
      return { ...state, openSidenav: action.value };
    }
    case "THEME": {
      theme = action.value;
      return { ...state, theme: action.value };
    }
    case "FONT": {
      font = action.value;
      return { ...state, font: action.value };
    }
    case "SIDENAV_TYPE": {
      return { ...state, sidenavType: action.value };
    }
    case "NAV_COLOR": {
      // set global color for the navbar
      return { ...state, navColor: action.value };
    }
    case "TRANSPARENT_NAVBAR": {
      return { ...state, transparentNavbar: action.value };
    }
    case "FIXED_NAVBAR": {
      return { ...state, fixedNavbar: action.value };
    }
    case "OPEN_CONFIGURATOR": {
      return { ...state, openConfigurator: action.value };
    }
    default: {
      throw new Error(`Unhandled action type: ${action.type}`);
    }
  }
}

export function MaterialTailwindControllerProvider({ children }) {
  const initialState = {
    openSidenav: false,
    navColor: "green",
    sidenavType: "white",
    transparentNavbar: true,
    fixedNavbar: false,
    openConfigurator: false,
    theme: localStorage.getItem("theme") || "light",
    font: localStorage.getItem("font") || "Roboto",
  };

  //el dispatch es el que se encarga de cambiar el estado, es un tipo de disparador de eventos

  const [controller, dispatch] = React.useReducer(reducer, initialState);
  const value = React.useMemo(
    () => [controller, dispatch],
    [controller, dispatch]
  );

  return (
    <MaterialTailwind.Provider value={value}>
      {children}
    </MaterialTailwind.Provider>
  );
}

export function useMaterialTailwindController() {
  const context = React.useContext(MaterialTailwind);

  if (!context) {
    throw new Error(
      "useMaterialTailwindController should be used inside the MaterialTailwindControllerProvider."
    );
  }

  return context;
}

MaterialTailwindControllerProvider.displayName = "/src/context/index.jsx";

MaterialTailwindControllerProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

export const setOpenSidenav = (dispatch, value) =>
  dispatch({ type: "OPEN_SIDENAV", value });
export const setTheme = (dispatch, value) => 
{
  localStorage.setItem("theme", value);
  dispatch({ type: "THEME", value });
}
//guarda el font en el local storage y no solo en el dispatch
export const setFont = (dispatch, value) =>
  {
   localStorage.setItem("font", value);
   dispatch({ type: "FONT", value });
  }
  
export const setNavColor = (dispatch, value) =>
  dispatch({ type: "NAV_COLOR", value });
export const setTransparentNavbar = (dispatch, value) =>
  dispatch({ type: "TRANSPARENT_NAVBAR", value });
export const setFixedNavbar = (dispatch, value) =>
  dispatch({ type: "FIXED_NAVBAR", value });
export const setOpenConfigurator = (dispatch, value) =>
  dispatch({ type: "OPEN_CONFIGURATOR", value });
