import PropTypes from "prop-types";
import { Link, NavLink } from "react-router-dom";
import { XMarkIcon } from "@heroicons/react/24/outline";
import {
  Avatar,
  Button,
  IconButton,
  Typography,
} from "@material-tailwind/react";
import { useMaterialTailwindController, setOpenSidenav } from "@/context";

import React, { useState, useEffect } from 'react';
import "amazon-connect-streams"

export function Sidenav({ brandImg, brandName, routes }) {
  const [controller, dispatch] = useMaterialTailwindController();
  const { sidenavColor, sidenavType, openSidenav } = controller;
  const sidenavTypes = {
    dark: "bg-gradient-to-br from-gray-800 to-gray-900",
    white: "bg-white shadow-sm",
    transparent: "bg-transparent",
  };
  
  
  useEffect(() => {
    let ccp_link = "https://igdrasilcallcenter.my.connect.aws/ccp-v2"
    let container_div = document.getElementById("container-div");
  
    connect.core.initCCP(container_div, {ccpUrl: ccp_link, softphone : {allowFramedSoftphone: true}, debug: true});
  }, []);

  return (
    <aside
      className={`${sidenavTypes[sidenavType]} ${
        openSidenav ? "translate-x-0" : "-translate-x-80"
      } fixed inset-0 z-50 my-4 ml-4 h-[calc(100vh-32px)] w-72 rounded-xl transition-transform duration-300 xl:translate-x-0 border border-blue-gray-100`}
    >
      <div id="container-div" className="w-full h-full"></div>
      
       {/*  <iframe src={ccp_link} id="iframe" allow="microphone; camera; autoplay; clipboard-write; identity-credentials-get"
        sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-downloads"
        className="w-full h-full" title="Contact Control Panel"/> */}

    </aside>
  );
}

Sidenav.defaultProps = {
  brandImg: "/img/logo-ct.png",
  brandName: "Material Tailwind React",
};

Sidenav.propTypes = {
  brandImg: PropTypes.string,
  brandName: PropTypes.string,
  routes: PropTypes.arrayOf(PropTypes.object).isRequired,
};

Sidenav.displayName = "/src/widgets/layout/sidnave.jsx";

export default Sidenav;
