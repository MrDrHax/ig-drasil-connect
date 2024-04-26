import React from "react";
import PropTypes from "prop-types";

export const MaterialTailwind = React.createContext(null);
MaterialTailwind.displayName = "MaterialTailwindContext";

export const navColors = {
  dark: "from-black to-black border-gray-200",
  green: "from-green-400 to-green-600",
  orange: "from-orange-400 to-orange-600",
  red: "from-red-400 to-red-600",
  pink: "from-pink-400 to-pink-600",
};

export function getBgColor(color) {
  const [controller, dispatch] = useMaterialTailwindController();
  const { theme } =
    controller;
  

  if (theme === "light") {
    switch (color) {
      case "dark":
        return "bg-gray-500";
      case "green":
        return "bg-green-500";
      case "orange":
        return "bg-orange-500";
      case "red":
        return "bg-red-500";
      case "pink":
        return "bg-pink-500";
      case "background":
        return "bg-white";
      case "background-cards":
        return "bg-white";
      case "search-bar":
        return "bg-black";
      default:
        return "bg-white";
    }
  } else {
    switch (color) {
      case "dark":
        return "bg-gray-100";
      case "green":
        return "bg-green-500";
      case "orange":
        return "bg-orange-500";
      case "red":
        return "bg-red-500";
      case "pink":
        return "bg-pink-500";
      case "background":
        return "bg-gray-900";
      case "background-cards":
        return "bg-gray-500";
      case "search-bar":
        return "bg-gray-800";
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
        return "text-black-900";
      case "green":
        return "text-green-500";
      case "white":
        return "text-gray-500";
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
        return "text-gray-500";
      case "green":
        return "text-green-500";
      case "orange":
        return "text-orange-500";
      case "red":
        return "text-red-500";
      case "pink":
        return "text-pink-500";
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
      return { ...state, theme: action.value };
    }
    case "FONT": {
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
    navColor: "dark",
    sidenavType: "white",
    transparentNavbar: true,
    fixedNavbar: false,
    openConfigurator: false,
    theme: "light",
    font: "Normal",
  };

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
  dispatch({ type: "THEME", value });
export const setFont = (dispatch, value) =>
  dispatch({ type: "FONT", value });
export const setNavColor = (dispatch, value) =>
  dispatch({ type: "NAV_COLOR", value });
export const setTransparentNavbar = (dispatch, value) =>
  dispatch({ type: "TRANSPARENT_NAVBAR", value });
export const setFixedNavbar = (dispatch, value) =>
  dispatch({ type: "FIXED_NAVBAR", value });
export const setOpenConfigurator = (dispatch, value) =>
  dispatch({ type: "OPEN_CONFIGURATOR", value });
