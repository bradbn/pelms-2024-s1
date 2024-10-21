PULSONIX_LIBRARY_ASCII "SamacSys ECAD Model"
//12748586/1373323/2.50/2/3/Connector

(asciiHeader
	(fileUnits MM)
)
(library Library_1
	(padStyleDef "s217.5_h145"
		(holeDiam 1.45)
		(padShape (layerNumRef 1) (padShapeType Rect)  (shapeWidth 2.175) (shapeHeight 2.175))
		(padShape (layerNumRef 16) (padShapeType Rect)  (shapeWidth 2.175) (shapeHeight 2.175))
	)
	(padStyleDef "c217.5_h145"
		(holeDiam 1.45)
		(padShape (layerNumRef 1) (padShapeType Ellipse)  (shapeWidth 2.175) (shapeHeight 2.175))
		(padShape (layerNumRef 16) (padShapeType Ellipse)  (shapeWidth 2.175) (shapeHeight 2.175))
	)
	(textStyleDef "Normal"
		(font
			(fontType Stroke)
			(fontFace "Helvetica")
			(fontHeight 1.27)
			(strokeWidth 0.127)
		)
	)
	(patternDef "MC000046" (originalName "MC000046")
		(multiLayer
			(pad (padNum 1) (padStyleRef s217.5_h145) (pt 0.000, 0.000) (rotation 90))
			(pad (padNum 2) (padStyleRef c217.5_h145) (pt 5.000, 0.000) (rotation 90))
		)
		(layerContents (layerNumRef 18)
			(attr "RefDes" "RefDes" (pt 2.250, -0.300) (textStyleRef "Normal") (isVisible True))
		)
		(layerContents (layerNumRef 28)
			(line (pt -2.5 4.8) (pt 7.5 4.8) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt 7.5 4.8) (pt 7.5 -5.4) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt 7.5 -5.4) (pt -2.5 -5.4) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt -2.5 -5.4) (pt -2.5 4.8) (width 0.025))
		)
		(layerContents (layerNumRef 18)
			(line (pt -2.5 4.8) (pt 7.5 4.8) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt 7.5 4.8) (pt 7.5 -5.4) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt 7.5 -5.4) (pt -2.5 -5.4) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt -2.5 -5.4) (pt -2.5 4.8) (width 0.2))
		)
		(layerContents (layerNumRef Courtyard_Top)
			(line (pt -4 5.8) (pt 8.5 5.8) (width 0.1))
		)
		(layerContents (layerNumRef Courtyard_Top)
			(line (pt 8.5 5.8) (pt 8.5 -6.4) (width 0.1))
		)
		(layerContents (layerNumRef Courtyard_Top)
			(line (pt 8.5 -6.4) (pt -4 -6.4) (width 0.1))
		)
		(layerContents (layerNumRef Courtyard_Top)
			(line (pt -4 -6.4) (pt -4 5.8) (width 0.1))
		)
		(layerContents (layerNumRef 28)
			(line (pt -2.5 2.8) (pt -3 2.8) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt -3 2.8) (pt -3 2.4) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt -3 2.4) (pt -2.5 2.4) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt -2.5 -4.4) (pt -3 -4.4) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt -3 -4.4) (pt -3 -4.8) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt -3 -4.8) (pt -2.5 -4.8) (width 0.025))
		)
		(layerContents (layerNumRef 18)
			(line (pt -2.5 2.4) (pt -3 2.4) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt -3 2.4) (pt -3 2.8) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt -3 2.8) (pt -2.5 2.8) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt -2.5 -4.8) (pt -3 -4.8) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt -3 -4.8) (pt -3 -4.4) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt -3 -4.4) (pt -2.5 -4.4) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt -3.4 0) (pt -3.4 0) (width 0.1))
		)
		(layerContents (layerNumRef 18)
			(arc (pt -3.35, 0) (radius 0.05) (startAngle 180.0) (sweepAngle 180.0) (width 0.1))
		)
		(layerContents (layerNumRef 18)
			(line (pt -3.3 0) (pt -3.3 0) (width 0.1))
		)
		(layerContents (layerNumRef 18)
			(arc (pt -3.35, 0) (radius 0.05) (startAngle .0) (sweepAngle 180.0) (width 0.1))
		)
	)
	(symbolDef "MC000046" (originalName "MC000046")

		(pin (pinNum 1) (pt 0 mils 0 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -25 mils) (rotation 0]) (justify "Left") (textStyleRef "Normal"))
		))
		(pin (pinNum 2) (pt 0 mils -100 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -125 mils) (rotation 0]) (justify "Left") (textStyleRef "Normal"))
		))
		(line (pt 200 mils 100 mils) (pt 600 mils 100 mils) (width 6 mils))
		(line (pt 600 mils 100 mils) (pt 600 mils -200 mils) (width 6 mils))
		(line (pt 600 mils -200 mils) (pt 200 mils -200 mils) (width 6 mils))
		(line (pt 200 mils -200 mils) (pt 200 mils 100 mils) (width 6 mils))
		(attr "RefDes" "RefDes" (pt 650 mils 300 mils) (justify Left) (isVisible True) (textStyleRef "Normal"))
		(attr "Type" "Type" (pt 650 mils 200 mils) (justify Left) (isVisible True) (textStyleRef "Normal"))

	)
	(compDef "MC000046" (originalName "MC000046") (compHeader (numPins 2) (numParts 1) (refDesPrefix J)
		)
		(compPin "1" (pinName "1") (partNum 1) (symPinNum 1) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "2" (pinName "2") (partNum 1) (symPinNum 2) (gateEq 0) (pinEq 0) (pinType Unknown))
		(attachedSymbol (partNum 1) (altType Normal) (symbolName "MC000046"))
		(attachedPattern (patternNum 1) (patternName "MC000046")
			(numPads 2)
			(padPinMap
				(padNum 1) (compPinRef "1")
				(padNum 2) (compPinRef "2")
			)
		)
		(attr "element14 Part Number" "")
		(attr "element14 Price/Stock" "")
		(attr "Manufacturer_Name" "Multicomp Pro")
		(attr "Manufacturer_Part_Number" "MC000046")
		(attr "Description" "Wire-To-Board Terminal Block, 5 mm, 2 Positions, 26 AWG, 12 AWG, Screw")
		(attr "<Hyperlink>" "")
		(attr "<Component Height>" "14.3")
	)

)
