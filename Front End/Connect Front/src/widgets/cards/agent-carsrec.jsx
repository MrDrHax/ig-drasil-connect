import {
    Card,
    CardHeader,
    CardBody,
    CardFooter,
    Typography,
  } from "@material-tailwind/react";
  import PropTypes from "prop-types";
  import { 
    getBgColor,
    useMaterialTailwindController, } from "@/context";

  {/* esta carta es para la informacion de los usuarios*/}
  export function CustomerCard({ name,descripcion, footer }) {
    const controller = useMaterialTailwindController();
    const theme = controller;

    return (
      <Card className={`border border-blue-gray-100 shadow-sm ${getBgColor("background-cards")}`}>
        <CardBody className="p-4 text-right">
          <Typography variant="h4" className="font-bold text-justify text-blue-gray-600" color={theme === "light"? 'black' : 'white'}>
            Data Customer
          </Typography>
          <Typography variant="paragraph" className=" p-1 text-justify text-blue-gray-600" color={theme === "light"? 'black' : 'white'}>
           <span className="font-bold text-blue-gray">Name of Customer: </span>{name}
          </Typography>
          <Typography variant="paragraph" className="p-1 text-left text-blue-gray-600" color={theme === "light"? 'black' : 'white'}>
           <span className="font-bold text-blue-gray">Situation: </span>{descripcion}
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
      <Card className="border border-blue-gray-100 shadow-sm">
        <CardBody className="p-4 text-right">
          <Typography variant="small" className="font-normal text-blue-gray-600">
            Lex Recommedation
          </Typography>
          <Typography variant="h4" color="blue-gray">
           Recommendation: {recomendation}
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