import React from "react";
import { 
        Card,
        Accordion,
        AccordionBody,  
        AccordionHeader} from "@material-tailwind/react";

export function RecomendationCard({title, content, id, openID, openhandler}) { 
    return(
      <Accordion open={openID == id} >
        <AccordionHeader onClick={() => openhandler(id)}>
          {title}
        </AccordionHeader>
        <AccordionBody>
          {content}
        </AccordionBody>
      </Accordion>
    )
}

export default RecomendationCard;