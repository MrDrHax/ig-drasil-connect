import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { Cog6ToothIcon } from "@heroicons/react/24/solid";
import { IconButton } from "@material-tailwind/react";
import {
  Sidenav,
  DashboardNavbar,
  Configurator,
  Footer,
} from "@/widgets/layout";
import routes from "@/routes";
import { useMaterialTailwindController, setOpenConfigurator, getBgColor } from "@/context";
import { validateToken, getApiLoginPage } from "@/configs";
import { AlertProvider } from "@/context/alerts";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI.
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // You can also log the error to an error reporting service
    console.log(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // You can render any custom fallback UI
      return (
        <div className="p-10">
          <h1>Something went wrong while loading the sub-page.</h1>
          <button onClick={this.handleReload}>Try Reloading</button>
        </div>
      );
    }

    return this.props.children;
  }
}

export function Dashboard() {
  if (validateToken()) {
    getApiLoginPage()
      .then(data => { console.log(data); window.location.href = data; })
      .catch(error => console.error('Error trying to get login link:', error));
    return <div>Redirecting...</div>;
  }

  const [controller, dispatch] = useMaterialTailwindController();
  const { sidenavType, theme } = controller;

  return (
    <div className={`min-h-screen ${getBgColor("background")}`}>
      <Sidenav
        routes={routes}
        brandImg={
          sidenavType === "dark" ? "/img/logo-ct.png" : "/img/logo-ct-dark.png"
        }
      />
      <div className="p-4 xl:ml-80">
        <DashboardNavbar />
        <Configurator />
        <IconButton
          size="lg"
          color="white"
          className="fixed bottom-8 right-8 z-40 rounded-full shadow-blue-gray-900/10"
          ripple={false}
          onClick={() => setOpenConfigurator(dispatch, true)}
        >
          <Cog6ToothIcon className="h-5 w-5" />
        </IconButton>
        <ErrorBoundary>
          <AlertProvider >
            <Routes>
              {routes.map(
                ({ layout, pages }) =>
                  layout === "dashboard" &&
                  pages.map(({ path, element }) => (
                    <Route exact path={path} element={element} />
                  ))
              )}
            </Routes>
          </AlertProvider >
        </ErrorBoundary>
        <div className="text-blue-gray-600">
          <Footer />
        </div>
      </div>
    </div>
  );
}

Dashboard.displayName = "/src/layout/dashboard.jsx";

export default Dashboard;
