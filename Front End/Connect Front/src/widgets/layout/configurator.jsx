import React from "react";
import { XMarkIcon } from "@heroicons/react/24/outline";
import {
  Button,
  ButtonGroup,
  IconButton,
  Switch,
  Typography,
} from "@material-tailwind/react";
import {
  useMaterialTailwindController,
  getBgColor, 
  getTextColor,
  setOpenConfigurator,
  setNavColor,
  setTheme,
  setFont,
  setFixedNavbar,
  navColors,
  getTheme,
  getFont,
  getTypography,
  getBorderColor,
} from "@/context";

function formatNumber(number, decPlaces) {
  decPlaces = Math.pow(10, decPlaces);

  const abbrev = ["K", "M", "B", "T"];

  for (let i = abbrev.length - 1; i >= 0; i--) {
    var size = Math.pow(10, (i + 1) * 3);

    if (size <= number) {
      number = Math.round((number * decPlaces) / size) / decPlaces;

      if (number == 1000 && i < abbrev.length - 1) {
        number = 1;
        i++;
      }

      number += abbrev[i];

      break;
    }
  }

  return number;
}

export function Configurator() {
  const [controller, dispatch] = useMaterialTailwindController();
  const { openConfigurator, navColor, font, theme, fixedNavbar } =
    controller;
  const [stars, setStars] = React.useState(0);

  React.useEffect(() => {
    const stars = fetch(
      "https://api.github.com/repos/creativetimofficial/material-tailwind-dashboard-react"
    )
      .then((response) => response.json())
      .then((data) => setStars(formatNumber(data.stargazers_count, 1)));
  }, []);

  return (
    <aside
      className={`fixed top-0 right-0 z-50 h-screen w-96  ${getBgColor("background-cards")} px-2.5 shadow-lg transition-transform duration-300 ${
        openConfigurator ? "translate-x-0" : "translate-x-96"
      }`}
    >
      <div className="flex items-start justify-between px-6 pt-8 pb-6">
        <div>
          <Typography variant="h5" className={`${getTypography()}  ${getTextColor('bgray')}`}>
            Dashboard Configurator
          </Typography>
          <Typography className={`${getTypography()}  ${getTextColor('gray')}`}>
            See our dashboard options.
          </Typography>
        </div>
        <IconButton
          variant="text"
          color="blue-gray"
          onClick={() => setOpenConfigurator(dispatch, false)}
        >
          <XMarkIcon strokeWidth={2.5} className="h-5 w-5" />
        </IconButton>
      </div>
      <div className="py-4 px-6">
        <div className="mb-12">
          <Typography variant="h6" className={`${getTypography()}  ${getTextColor('bgray')}`}>
            Nav colors
          </Typography>
          <div className="mt-3 flex items-center gap-2">
            {Object.keys(navColors).map((color) => (
              <span
                key={color}
                className={`h-6 w-6 cursor-pointer rounded-full border bg-gradient-to-br transition-transform hover:scale-105 ${
                  navColors[color]
                } ${
                  navColor === color ? "border-black" : "border-transparent"
                }`}
                onClick={() => setNavColor(dispatch, color)}
              />
            ))}
          </div>
        </div>
        <div className="mb-12">
          <Typography variant="h6" className={`${getTypography()}  ${getTextColor('dark')}`}>
            Font type
          </Typography>
          <Typography variant="small" className={`${getTypography()}  ${getTextColor('gray')}`}>
            Choose between a dislexyc accesible font and normal font.
          </Typography>

          {/* Font selector */}

          <div className={`mt-3 flex items-center gap-2 ${getTypography()}  ${getTextColor('gray')}`}>
            <Button
              className={`${getTextColor('contrast')} ${getTypography()} ${getFont() === "OpenDyslexic" ? getBgColor(navColor) : getBgColor("background")}`}
              // variant={font === "OpenDyslexic" ? "gradient" : "outlined"}
              onClick={() => setFont(dispatch, "OpenDyslexic")}
            >
              OpenDyslexic
            </Button>
            <Button
              className={`${getTextColor('contrast')} ${getTypography()} ${getFont() === "Normal" ? getBgColor(navColor) : getBgColor("background")}`}
              // variant={font === "Normal" ? "gradient" : "outlined"}
              onClick={() => setFont(dispatch, "Normal")}
            >
              Normal
            </Button>
          </div>


        </div>
        <div className="mb-12">
          <Typography variant="h6" className={`${getTypography()} ${getTextColor('dark')}`}>
            Color pallete
          </Typography>
          <Typography variant="small" className={`${getTypography()} ${getTextColor('gray')}`}>
            Choose between dark and light modes.
          </Typography>


          {/* Theme selector */}

          <div className={`mt-3 flex items-center gap-2 ${getTextColor('gray')}`}>
            <Button
              className= {`${getTextColor('contrast')} ${getTypography()} ${getTheme() === "dark" ? getBgColor(navColor) : getBgColor("background")}`}
              onClick={() => setTheme(dispatch, "dark")}
            >
              Dark
            </Button>
            <Button
              className= {`${getTextColor('contrast')} ${getTypography()} ${getTheme() === "light" ? getBgColor(navColor) : getBgColor("background")}`}
              onClick={() => setTheme(dispatch, "light")}
            >
              Light
            </Button>
          </div>


        </div>
        <div className="mb-12">
          <hr />
          <div className="flex items-center justify-between py-5">
            <Typography variant="h6" className={`${getTypography()} ${getTextColor('gray')}`}>
              Navbar Fixed
            </Typography>
            <Switch
              id="navbar-fixed"
              value={fixedNavbar}
              onChange={() => setFixedNavbar(dispatch, !fixedNavbar)}
            />
          </div>
          <hr />
          </div>
      </div>
    </aside>
  );
}

Configurator.displayName = "/src/widgets/layout/configurator.jsx";

export default Configurator;
