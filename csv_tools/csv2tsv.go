package main

import (
	"bufio"
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"strings"
	"time"
)

func main() {
	inputFilePath := "/Users/tis/foam/cdp/data/turo.csv"
	outputFilePath := "/Users/tis/foam/cdp/data/turogo.tsv"

	// Get the start time
	startTime := time.Now()

	// Open the input CSV file
	csvFile, err := os.Open(inputFilePath)
	if err != nil {
		fmt.Println("Error opening CSV file:", err)
		return
	}
	defer csvFile.Close()

	// Create the output TSV file
	tsvFile, err := os.Create(outputFilePath)
	if err != nil {
		fmt.Println("Error creating TSV file:", err)
		return
	}
	defer tsvFile.Close()

	// Create a buffered reader to handle BOM removal
	reader := bufio.NewReader(csvFile)

	// Read and discard the BOM (if present) at the beginning of the file
	bom := []byte{0xef, 0xbb, 0xbf}
	prefix, err := reader.Peek(3)
	if err != nil {
		fmt.Println("Error reading file:", err)
		return
	}
	if len(prefix) >= 3 && prefix[0] == bom[0] && prefix[1] == bom[1] && prefix[2] == bom[2] {
		_, err = reader.Discard(3)
		if err != nil {
			fmt.Println("Error discarding BOM:", err)
			return
		}
	}

	// Create a new CSV reader with relaxed parsing rules
	csvReader := csv.NewReader(reader)
	csvReader.LazyQuotes = true // Allows unescaped quotes within fields

	// Create a new TSV writer
	writer := csv.NewWriter(tsvFile)
	writer.Comma = '\t' // Set the delimiter to tab for TSV

	// Read and write each row
	for {
		record, err := csvReader.Read()
		if err == io.EOF {
			// End of file
			break
		} else if err != nil {
			fmt.Println("Error reading CSV record:", err)
			return
		}

		// Remove BOM from the "Address" field (and any other field)
		for i, field := range record {
			record[i] = strings.Replace(field, "\ufeff", "", -1)
		}

		// Write the modified record to the TSV file
		err = writer.Write(record)
		if err != nil {
			fmt.Println("Error writing TSV record:", err)
			return
		}
	}

	// Flush the writer to ensure all data is written
	writer.Flush()

	// Get the end time and calculate the elapsed time
	endTime := time.Now()
	elapsedTime := endTime.Sub(startTime)

	fmt.Println("CSV to TSV conversion complete. Output file:", outputFilePath)
	fmt.Printf("Conversion took %v\n", elapsedTime)
}
