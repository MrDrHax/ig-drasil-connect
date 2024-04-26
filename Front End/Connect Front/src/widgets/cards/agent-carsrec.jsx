import {
    Card,
    CardHeader,
    CardBody,
    CardFooter,
    Typography,
  } from "@material-tailwind/react";
  import PropTypes from "prop-types";
  import { 
    getBgColor, // estos 2 jalan los colores necesarios del contexto
    getTextColor, 
    useMaterialTailwindController, } from "@/context";

  {/* esta carta es para la informacion de los usuarios*/}
  export function CustomerCard({ name,description, footer }) {
    const controller = useMaterialTailwindController();
    const theme = controller;
    {/* En los className llaman a la función que esta manejando el background o el color de texto */}
    return (
      <Card className={`border border-blue-gray-100 shadow-sm ${getBgColor("background-cards")}`}>
        <CardBody className="p-4 text-right">
          <Typography variant="h4" className={`font-bold text-justify text-blue-gray-600 ${getTextColor("dark")}`}>
            Data Customer
          </Typography>
          <Typography variant="paragraph" className={`text-justify text-blue-gray-600 ${getTextColor("dark")}`}>
           <span className="font-bold text-blue-gray">Name of Customer: </span> {name}
          </Typography>
          <Typography variant="paragraph" className={`text-justify text-blue-gray-600 ${getTextColor("dark")}`}>
           <span className="font-bold text-blue-gray">Condition: </span> {description}
          </Typography>
        </CardBody>
        {footer && (
          <CardFooter className={`border-t border-blue-gray-50 p-4 ${getTextColor("dark")}`}>
            {footer}
          </CardFooter>
        )}
      </Card>
    );
  }
  
  CustomerCard.defaultProps = {
    color: "blue",
    footer: null,
  };
  
  CustomerCard.propTypes = {
    color: PropTypes.oneOf([
      "white",
      "blue-gray",
      "gray",
      "brown",
      "deep-orange",
      "orange",
      "amber",
      "yellow",
      "lime",
      "light-green",
      "green",
      "teal",
      "cyan",
      "light-blue",
      "blue",
      "indigo",
      "deep-purple",
      "purple",
      "pink",
      "red",
    ]),
    icon: PropTypes.node.isRequired,
    title: PropTypes.node.isRequired,
    value: PropTypes.node.isRequired,
    footer: PropTypes.node,
  };
  
  CustomerCard.displayName = "/src/widgets/cards/statistics-card.jsx";
  
  export function Lexcard({ recomendation, footer }) {
    return (
      <Card className={`border border-blue-gray-100 shadow-sm ${getBgColor("background-cards")}`}>
        <CardBody className="p-4 text-right">
          <Typography variant="h4" className={`font-bold text-justify text-blue-gray-600 ${getTextColor("dark")}`} >
            Al/n, your virtual assistant:
          </Typography>
          <Typography variant="paragraph" className={`p-1 text-justify text-blue-gray-600 ${getTextColor("dark")}`}>
          <span className="font-bold text-blue-gray"> Recommends: </span> {recomendation} 😊
          </Typography>
        </CardBody>
        {footer && (
          <CardFooter className="border-t border-blue-gray-50 p-4">
            {footer}
          </CardFooter>
        )}
      </Card>
    );
  }
  
  Lexcard.defaultProps = {
    color: "blue",
    footer: null,
  };
  
  Lexcard.propTypes = {
    color: PropTypes.oneOf([
      "white",
      "blue-gray",
      "gray",
      "brown",
      "deep-orange",
      "orange",
      "amber",
      "yellow",
      "lime",
      "light-green",
      "green",
      "teal",
      "cyan",
      "light-blue",
      "blue",
      "indigo",
      "deep-purple",
      "purple",
      "pink",
      "red",
    ]),
    icon: PropTypes.node.isRequired,
    title: PropTypes.node.isRequired,
    value: PropTypes.node.isRequired,
    footer: PropTypes.node,
  };
  
  Lexcard.displayName = "/src/widgets/cards/statistics-card.jsx";

  export default CustomerCard; Lexcard;