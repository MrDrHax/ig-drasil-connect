import React from "react";
import { 
        Card,
        Accordion,
        AccordionBody,  
        AccordionHeader} from "@material-tailwind/react";
import { getBgColor, getTextColor, useMaterialTailwindController,getTypography,getTypographybold } from "@/context";

export function RecomendationCard({title, content, id, openID, openhandler}) { 
  const controller = useMaterialTailwindController();
    return(
      <Accordion open={openID == id} >
        <AccordionHeader onClick={() => openhandler(id)}>
          <span className={`${getTypographybold()} ${getTextColor("white3")} `}>{title}</span>
        </AccordionHeader>
        <AccordionBody>
          <span className={`${getTypography()} ${getTextColor("white3")} `}>{content}</span>
        </AccordionBody>
      </Accordion>
    )
}

export default RecomendationCard;