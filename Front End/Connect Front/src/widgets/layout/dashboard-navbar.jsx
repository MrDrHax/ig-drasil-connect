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
  HomeIcon
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
  getBorderColor,
} from "@/context";
import { getApiLoginPage, getNameFromToken, getRolesFromToken } from "@/configs";

import { AgentId } from '@/data';

import { Notifications } from '@/pages/dashboard';

import { Alerts } from '@/data/supervisor-home-data';

function handleTabClick(tab) {
  history.push(`/${tab}`);
}

export function DashboardNavbar() {
  const [controller, dispatch] = useMaterialTailwindController();
  const { navColor, fixedNavbar, openSidenav, theme } = controller;
  const { pathname } = useLocation();
  const [layout, page] = pathname.split("/").filter((el) => el !== "");

  const [agent_id, setAgent_id] = useState('');

  const [gotNotification, setGotNotification] = useState(false);

  const [info, setInfo] = useState([]);

  const roles = getRolesFromToken();

  function getNotifications(isAgent, isSupervisor) {

    if (isAgent) {
      Alerts(false, agent_id).then((data) => {
        setInfo(data);
      });
    }

    if (isSupervisor) {
      Alerts(true, agent_id).then((data) => {
        setInfo(info.concat(data));
      });
    }

    setGotNotification(true);

  }

  useEffect(() => {
    AgentId().then((data) => {
      setAgent_id(data);
    });

    if (!gotNotification)
      getNotifications(roles.includes('agent'), roles.includes('manager'));
  }, []);

  return (
    <Navbar
      color= {"transparent"}
      className={`rounded-xl transition-all ${fixedNavbar
        ? `sticky top-4 z-40 py-3 shadow-md shadow-blue-gray-500/5 ${getBgColor('background')}`
        : "px-0 py-1"
        }`}
      fullWidth
      blurred={fixedNavbar}
    >
      <div className="flex flex-col-reverse justify-between gap-6 md:flex-row md:items-center">
        <div className="capitalize">

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
          <IconButton
            variant="text"
            color="blue-gray"
            className="grid xl:hidden"
            onClick={() => setOpenSidenav(dispatch, !openSidenav)}
          >
            <Bars3Icon strokeWidth={3} className="h-6 w-6 text-blue-gray-500" />
          </IconButton>

          {/* Profile dropdown */}
          <Tooltip placement="bottom" className={`border ${getBorderColor('dark')} bg-white px-4 py-3 shadow-xl shadow-black/10 ${getBgColor('background')}`}
          content={ <div className="w-80">
                      <Typography color="blue-gray" className={`font-medium ${getTypography()} ${getTextColor("contrast")}`}>
                        {getNameFromToken()}
                      </Typography>
                      {roles.map((role, index) => (
                        <Typography
                          key={index}
                          variant="small"
                          color="blue-gray"
                          className={`font-normal opacity-80 ${getTypography()} ${getTextColor("contrast")}`}
                        >
                          {role == "manager" ? "Supervisor" : role == "agent" ? "Agent" : null}
                        </Typography>
                      ))}
                    </div>}>
              <Button
                variant="text"
                color="blue-gray"
                className={`hidden items-center gap-1 px-4 xl:flex normal-case ${getTypography()} ${getTextColor("contrast")}`}
              >
                <UserCircleIcon className={`h-5 w-5 ${getTextColor("contrast")}`} />
                {getNameFromToken()}
              </Button>              
          </Tooltip>

          {/* Notifications */}
          <Menu placement="bottom">
          <MenuHandler>
            <IconButton variant="text" color="blue-gray" className="hidden xl:flex">
              <BellIcon className={`h-5 w-5 ${getTextColor("contrast")}`} />
              { info.length == 0 ? null :
              <div key="Num_Notifications" className={`absolute bottom-0 right-0 rounded-full bg-red-600 w-2.5 h-2.5 ${getTextColor("contrast")}`}/>
              }
            </IconButton>
          </MenuHandler>
          <MenuList className={`${getBgColor("background")} ${getBorderColor("dark")}`}>
              {
                info.map(({Text,TextRecommendation, color, timestamp }) => (
                  <MenuItem key={timestamp} className="flex items-center gap-3">
                      <Typography
                        variant="small"
                        className={ `mb-1 ${getTypography()} ${getTextColor("contrast")}` }
                      >
                        <strong className={ `${getTypographybold()} ${getTextColor(color)}` }>{Text}</strong> <br /><span className={ `${getTypographybold()} ${getTextColor("contrast")}` }>Recommendation: </span>{TextRecommendation}
                      </Typography>
                    </MenuItem>
                ))
              }
          </MenuList>
          </Menu>

          {/* Configurator button */}
          <IconButton
            variant="text"
            color="blue-gray"
            className='p-2 mr-1'
            onClick={() => setOpenConfigurator(dispatch, true)}
          >
            <Cog6ToothIcon className={`h-5 w-5  ${getTextColor("contrast")}`} />
          </IconButton>

          {/* Link to aws portal */}
          <Link to = {'https://igdrasilconnect.awsapps.com/start/#/?tab=applications'}>
            <IconButton
            variant="text"
            color="black"
            className={`p-2 mr-1`}
            >
              <HomeIcon className={`h-5 w-5 ${getTextColor("contrast")}`} />
            </IconButton>
          </Link>
            
        </div>
      </div>
    </Navbar>
  );
}

DashboardNavbar.displayName = "/src/widgets/layout/dashboard-navbar.jsx";

export default DashboardNavbar;
