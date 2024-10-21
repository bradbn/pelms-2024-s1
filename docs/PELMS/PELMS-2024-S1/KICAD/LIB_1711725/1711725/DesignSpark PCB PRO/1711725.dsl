SamacSys ECAD Model
12791287/1373323/2.50/2/2/Connector

DESIGNSPARK_INTERMEDIATE_ASCII

(asciiHeader
	(fileUnits MM)
)
(library Library_1
	(padStyleDef "s195_h130"
		(holeDiam 1.3)
		(padShape (layerNumRef 1) (padShapeType Rect)  (shapeWidth 1.950) (shapeHeight 1.950))
		(padShape (layerNumRef 16) (padShapeType Rect)  (shapeWidth 1.950) (shapeHeight 1.950))
	)
	(padStyleDef "c195_h130"
		(holeDiam 1.3)
		(padShape (layerNumRef 1) (padShapeType Ellipse)  (shapeWidth 1.950) (shapeHeight 1.950))
		(padShape (layerNumRef 16) (padShapeType Ellipse)  (shapeWidth 1.950) (shapeHeight 1.950))
	)
	(textStyleDef "Default"
		(font
			(fontType Stroke)
			(fontFace "Helvetica")
			(fontHeight 50 mils)
			(strokeWidth 5 mils)
		)
	)
	(patternDef "1711725" (originalName "1711725")
		(multiLayer
			(pad (padNum 1) (padStyleRef s195_h130) (pt 0.000, 0.000) (rotation 90))
			(pad (padNum 2) (padStyleRef c195_h130) (pt 5.080, 0.000) (rotation 90))
		)
		(layerContents (layerNumRef 18)
			(attr "RefDes" "RefDes" (pt 2.540, 0.300) (textStyleRef "Default") (isVisible True))
		)
		(layerContents (layerNumRef 28)
			(line (pt -2.54 5.9) (pt 7.62 5.9) (width 0.2))
		)
		(layerContents (layerNumRef 28)
			(line (pt 7.62 5.9) (pt 7.62 -5.3) (width 0.2))
		)
		(layerContents (layerNumRef 28)
			(line (pt 7.62 -5.3) (pt -2.54 -5.3) (width 0.2))
		)
		(layerContents (layerNumRef 28)
			(line (pt -2.54 -5.3) (pt -2.54 5.9) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt -2.54 5.9) (pt 7.62 5.9) (width 0.1))
		)
		(layerContents (layerNumRef 18)
			(line (pt 7.62 5.9) (pt 7.62 -5.3) (width 0.1))
		)
		(layerContents (layerNumRef 18)
			(line (pt 7.62 -5.3) (pt -2.54 -5.3) (width 0.1))
		)
		(layerContents (layerNumRef 18)
			(line (pt -2.54 -5.3) (pt -2.54 5.9) (width 0.1))
		)
		(layerContents (layerNumRef 30)
			(line (pt -3.54 6.9) (pt 8.62 6.9) (width 0.1))
		)
		(layerContents (layerNumRef 30)
			(line (pt 8.62 6.9) (pt 8.62 -6.3) (width 0.1))
		)
		(layerContents (layerNumRef 30)
			(line (pt 8.62 -6.3) (pt -3.54 -6.3) (width 0.1))
		)
		(layerContents (layerNumRef 30)
			(line (pt -3.54 -6.3) (pt -3.54 6.9) (width 0.1))
		)
	)
	(symbolDef "1711725" (originalName "1711725")

		(pin (pinNum 1) (pt 0 mils 0 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -25 mils) (rotation 0]) (justify "Left") (textStyleRef "Default"))
		))
		(pin (pinNum 2) (pt 0 mils -100 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -125 mils) (rotation 0]) (justify "Left") (textStyleRef "Default"))
		))
		(line (pt 200 mils 100 mils) (pt 600 mils 100 mils) (width 6 mils))
		(line (pt 600 mils 100 mils) (pt 600 mils -200 mils) (width 6 mils))
		(line (pt 600 mils -200 mils) (pt 200 mils -200 mils) (width 6 mils))
		(line (pt 200 mils -200 mils) (pt 200 mils 100 mils) (width 6 mils))
		(attr "RefDes" "RefDes" (pt 650 mils 300 mils) (justify Left) (isVisible True) (textStyleRef "Default"))

	)
	(compDef "1711725" (originalName "1711725") (compHeader (numPins 2) (numParts 1) (refDesPrefix J)
		)
		(compPin "1" (pinName "1") (partNum 1) (symPinNum 1) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "2" (pinName "2") (partNum 1) (symPinNum 2) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(attachedSymbol (partNum 1) (altType Normal) (symbolName "1711725"))
		(attachedPattern (patternNum 1) (patternName "1711725")
			(numPads 2)
			(padPinMap
				(padNum 1) (compPinRef "1")
				(padNum 2) (compPinRef "2")
			)
		)
		(attr "element14 Part Number" "")
		(attr "element14 Price/Stock" "")
		(attr "Manufacturer_Name" "Phoenix Contact")
		(attr "Manufacturer_Part_Number" "1711725")
		(attr "Description" "PCB terminal block, nominal current: 24 A, rated voltage (III/2): 400 V, nominal cross section: 2.5 mm?, Number of potentials: 2, Number of rows: 1, Number of positions per row: 2, product range: MKDS 3, pitch: 5.08 mm, connection method: Screw connection with tension sleeve, mounting: Wave soldering, conductor/PCB connection direction: 0 ?, color: green, Pin layout: Linear pinning, Solder pin [P]: 5 mm, type of packaging: packed in cardboard. The article can be aligned to create different nos. of positions")
		(attr "Datasheet Link" "http://www.phoenixcontact.net/product/1711725")
		(attr "Height" "18.2 mm")
	)

)
