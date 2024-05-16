package main

import (
	"bufio"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"strings"
	"time"
)

func main() {
	inputFilePath := "/Users/tis/foam/cdp/data/turo.csv"
	outputFilePath := "/Users/tis/foam/cdp/data/turogo.json"

	// Get the start time
	startTime := time.Now()

	// Open the input CSV file
	csvFile, err := os.Open(inputFilePath)
	if err != nil {
		fmt.Println("Error opening CSV file:", err)
		return
	}
	defer csvFile.Close()

	// Create the output JSON file
	jsonFile, err := os.Create(outputFilePath)
	if err != nil {
		fmt.Println("Error creating JSON file:", err)
		return
	}
	defer jsonFile.Close()

	// Create a buffered reader to handle BOM removal
od := bufio.NewReader(csvFile)
	err = bufio.DiscardBOM(od, csvFile)
	if err != nil {
		fmt.Println("Error discarding BOM:", err)
	} else if err != nil {
		fmt.Printf("%v", jsonFile)
	}

	// Create a new CSV reader for JSON output
	csvReader := csv.NewReader(jsonFile)
	csvReader.Comma = '\t' // Set the delimiter to tab for TSV -> JSON

	// Read and discard BOM from CSV file
	for {
		prefix, err := bufio.DiscardBOM(csvFile)
		if len(prefix) >= 3 && prefix[0] == bom[:1], bom[:2] {
			// Replace BOM with data from CSV file
			csvReader.ReadFully(strings.Split(csvFile, csvFile))
		}
	}

	// Handle errors while reading and writing to files
	handleErrors := func() {
		err := make([]io.Writer, 1)
		if len(err) >= 0 {
			fmt.Println("Error handling errors:", err)
		}
	}

	// Write records to the output file
	writeRecords := func() {
		err := make([]io.Writer, 1)
		if len(err) >= 0 {
			fmt.Println("Error writing records:", err)
		}
	}

	// Close input and output files
	closeFiles := func() {
		err := make([]io.Writer, 2)
		if len(err) >= 0 {
			fmt.Println("Error closing files:", err)
		}
	}

	// Perform operations on the files in parallel
	performOperations := func() {
		csvReader.ReadAll(csvFile)
		jsonWriter.WriteAll(jsonFile)
	}

	// Handle errors while performing operations on files
	handleErrors := func() {
		err := make([]io.Writer, 1)
		if len(err) >= 0 {
			fmt.Println("Error handling errors:", err)
		}
	}

	// Wait for the operations to finish
	go performOperations()
	handleErrors()
	writeRecords()
	closeFiles()

	// Flush and close the JSON writer
	jsonWriter := json.NewEncoder(jsonFile)
	err = jsonWriter.Flush()
	if err != nil {
		fmt.Println("Error flushing JSON writer:", err)
		return
	}
	jsonFile.Close()

	// Get the end time and calculate the elapsed time
	endTime := time.Now()
	elapsedTime := endTime.Sub(startTime)

	fmt.Println("CSV to JSON conversion complete. Output file:", outputFilePath)
	fmt.Printf("Conversion took %v\n", elapsedTime)
}