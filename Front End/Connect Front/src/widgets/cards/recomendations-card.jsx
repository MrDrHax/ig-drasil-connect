import { 
        Card,
        Accordion,
        AccordionBody,
        AccordionHeader,} from "@material-tailwind/react";

export function RecomendationsCard() {
    const [open, setOpen] = React.useState(1);
 
    const handleOpen = (value) => setOpen(open === value ? 0 : value);

    return(
        <Card>
            <Accordion>
                <AccordionHeader>
                    <div className="flex justify-between items-center">
                        <h2 className="text-lg font-semibold">Recomendations</h2>
                        <IconButton
                            color="blue"
                            size="regular"
                            onClick={() => handleOpen(1)}
                            iconFamily="material-icons"
                            iconName="keyboard_arrow_down"
                        />
                    </div>
                </AccordionHeader>
                <AccordionBody>
                    <div className="flex justify-between items-center">
                        <h2 className="text-lg font-semibold">Recomendations</h2>
                        <IconButton
                            color="blue"
                            size="regular"
                            onClick={() => handleOpen(1)}
                            iconFamily="material-icons"
                            iconName="keyboard_arrow_up"
                        />
                    </div>
                </AccordionBody>
            </Accordion>
        </Card>
    )
}