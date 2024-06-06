import React, { useState, useEffect } from 'react';
import ReactDOMServer from 'react-dom/server';
import { useLocation, Link } from "react-router-dom";
import {
  Navbar,
  Typography,
  Button,
  IconButton,
  Breadcrumbs,
  Input,
  Menu,
  MenuHandler,
  MenuList,
  MenuItem,
  Avatar,
  Tooltip
} from "@material-tailwind/react";
import {
  UserCircleIcon,
  Cog6ToothIcon,
  BellIcon,
  ClockIcon,
  CreditCardIcon,
  Bars3Icon,
} from "@heroicons/react/24/solid";
import {
  useMaterialTailwindController,
  setOpenConfigurator,
  setOpenSidenav,
  getBgColor,
  getTextColor,
  getTheme,
  getTypography,
  getTypographybold,
} from "@/context";
import { getApiLoginPage, getNameFromToken } from "@/configs";


import {getRolesFromToken} from '@/configs/api-tools';

function handleTabClick(tab) {
  history.push(`/${tab}`);
}

export function DashboardNavbar() {
  const [controller, dispatch] = useMaterialTailwindController();
  const { navColor, fixedNavbar, openSidenav, theme } = controller;
  const { pathname } = useLocation();
  const [layout, page] = pathname.split("/").filter((el) => el !== "");

  const [loginUrl, setLoginUrl] = useState('');

  let roles = getRolesFromToken();

  useEffect(() => {
    getApiLoginPage()
      .then(data => setLoginUrl(data))
      .catch(error => console.error('Error:', error));
  }, []);

  return (
    <Navbar
      color= {"transparent"}
      className={`rounded-xl transition-all ${fixedNavbar
        ? "sticky top-4 z-40 py-3 shadow-md shadow-blue-gray-500/5"
        : "px-0 py-1"
        }`}
      fullWidth
      blurred={fixedNavbar}
    >
      <div className="flex flex-col-reverse justify-between gap-6 md:flex-row md:items-center">
        <div className="capitalize">
          {/* <Breadcrumbs
            className={`bg-transparent p-0 transition-all ${
              fixedNavbar ? "mt-1" : ""
            }`}
          >
            <Link to={`/${layout}`}>
              <Typography
                variant="small"
                color="blue-gray"
                className="font-normal opacity-50 transition-all hover:text-blue-500 hover:opacity-100"
              >
                le test
              </Typography>
            </Link>
            <Typography
              variant="small"
              color="blue-gray"
              className="font-normal"
            >
              {page}
            </Typography>
          </Breadcrumbs> */}
          {/* <Typography variant="h6" color="blue-gray">
            {page}
          </Typography> */}

          <Typography variant="h6" className={'${getTypography()}'} color={getTheme() === "light"? 'black' : 'white'}>
          {/* Main navbar with tabs for different pages */}
            <div className="flex text-center">

              {/* Supervisor Tabs */}
              { roles.includes('manager') && (
                <>
                <Link
                  to="/dashboard/home"
                  className={`navitemAdmin rounded-xl flex-initial w-32 cursor-pointer ${getTypographybold()} ${page === 'home' ? getBgColor(navColor) + ' '+ getTextColor("white2") : ''}`}
                >
                  Home
                </Link>
                <Link
                  to="/dashboard/team"
                  className={`navitemAdmin rounded-xl flex-initial w-32 cursor-pointer ${getTypographybold()} ${page === 'team' ? getBgColor(navColor) + ' '+ getTextColor("white2") : ''}`}
                >
                  Agents
                </Link>
                <Link
                  to="/dashboard/queues"
                  className={`navitemAdmin rounded-xl flex-initial w-32 cursor-pointer ${getTypographybold()} ${page === 'queues' ? getBgColor(navColor) + ' '+ getTextColor("white2") : ''}`}
                >
                  Queues
                </Link>
                </>
              )}

              {/* Agent Tabs */}
              { roles.includes('agent') && (
                <Link
                  to="/dashboard/agent"
                  className={`navitemAdmin rounded-xl flex-initial w-32 cursor-pointer ${getTypographybold()} ${page === 'agent' ? getBgColor(navColor) + ' '+ getTextColor("white2") : ''}`}
                >
                  Dashboard
                </Link>
              )}
            </div>
          </Typography>


        </div>
        <div className="flex items-center">
          {/*
         <div className="mr-auto md:mr-4 md:w-56">
            <Input label="Search" />
          </div>
         */}
          <IconButton
            variant="text"
            color="blue-gray"
            className="grid xl:hidden"
            onClick={() => setOpenSidenav(dispatch, !openSidenav)}
          >
            <Bars3Icon strokeWidth={3} className="h-6 w-6 text-blue-gray-500" />
          </IconButton>

          {/* Profile dropdown */}
          <Tooltip placement="bottom" content="Profile">
            <>
              <Button
                variant="text"
                color="blue-gray"
                className={`hidden items-center gap-1 px-4 xl:flex normal-case ${getTypography()} ${getTextColor("contrast")}`}
              >
                <UserCircleIcon className={`h-5 w-5 ${getTextColor("contrast")}`} />
                {getNameFromToken()}
              </Button>
              <IconButton
                variant="text"
                color="blue-gray"
                className="grid xl:hidden"
              >
                <UserCircleIcon className={`h-5 w-5  ${getTextColor("contrast")}`} />
              </IconButton>
            </>
          </Tooltip>
          <Menu>
            <MenuHandler>
              <IconButton variant="text" color="blue-gray">
                <BellIcon className={`h-10 w-5 ${getTextColor("contrast")}`} />
              </IconButton>
            </MenuHandler>
            <MenuList className="w-max border-0">
              <MenuItem className="flex items-center gap-3">
                <Avatar
                  src="https://demos.creative-tim.com/material-dashboard/assets/img/team-2.jpg"
                  alt="item-1"
                  size="sm"
                  variant="circular"
                />
                <div>
                  <Typography
                    variant="small"
                    color="blue-gray"
                    className="mb-1 font-normal"
                  >
                    <strong>agent 1</strong> has connected a call
                  </Typography>
                  <Typography
                    variant="small"
                    color="blue-gray"
                    className="flex items-center gap-1 text-xs font-normal opacity-60"
                  >
                    <ClockIcon className="h-3.5 w-3.5" /> 13 minutes ago
                  </Typography>
                </div>
              </MenuItem>
              <MenuItem className="flex items-center gap-4">
                <Avatar
                  src="https://imgs.search.brave.com/YHSiLIxYYxfQCMAe51EOOPS0oevNKqtWXeUyDvJF7mU/rs:fit:860:0:0/g:ce/aHR0cHM6Ly9pMC53/cC5jb20vbmV3c3Bh/Y2stZWxzb2wuczMu/YW1hem9uYXdzLmNv/bS93cC1jb250ZW50/L3VwbG9hZHMvMjAy/NC8wNC9NYXBhY2hl/LVBlZHJvLmpwZz9m/aXQ9ODMwLDYyMyZz/c2w9MQ"
                  alt="item-1"
                  size="sm"
                  variant="circular"
                />
                <div>
                  <Typography
                    variant="small"
                    color="blue-gray"
                    className="mb-1 font-normal"
                  >
                    <strong>Issue with</strong> agent pedro
                  </Typography>
                  <Typography
                    variant="small"
                    color="blue-gray"
                    className="flex items-center gap-1 text-xs font-normal opacity-60"
                  >
                    <ClockIcon className="h-3.5 w-3.5" /> 1 day ago
                  </Typography>
                </div>
              </MenuItem>
              <MenuItem className="flex items-center gap-4">
                <div className="grid h-9 w-9 place-items-center rounded-full bg-gradient-to-tr from-blue-gray-800 to-blue-gray-900">
                  <CreditCardIcon className="h-4 w-4 text-white" />
                </div>
                <div>
                  <Typography
                    variant="small"
                    color="blue-gray"
                    className="mb-1 font-normal"
                  >
                    Payment successfully completed
                  </Typography>
                  <Typography
                    variant="small"
                    color="blue-gray"
                    className="flex items-center gap-1 text-xs font-normal opacity-60"
                  >
                    <ClockIcon className="h-3.5 w-3.5" /> 2 days ago
                  </Typography>
                </div>
              </MenuItem>
            </MenuList>
          </Menu>
          <IconButton
            variant="text"
            color="blue-gray"
            onClick={() => setOpenConfigurator(dispatch, true)}
          >
            <Cog6ToothIcon className={`h-5 w-5  ${getTextColor("contrast")}`} />
          </IconButton>
        </div>
      </div>
    </Navbar>
  );
}

DashboardNavbar.displayName = "/src/widgets/layout/dashboard-navbar.jsx";

export default DashboardNavbar;
