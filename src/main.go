package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"os"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"

	"dagger.io/dagger"
)

func main() {
	initLog()

	ctx := context.Background()
	if err := CollectParameters(ctx); err != nil {
		panic(err)
	}
	if err := VerifyParameters(ctx); err != nil {
		panic(err)
	}
}

func VerifyParameters(ctx context.Context) error {
	log.Info().Msg("Verifying parameters")

	return nil
}

func CollectParameters(ctx context.Context) error {
	// Initialize Dagger client
	client, err := dagger.Connect(ctx, dagger.WithLogOutput(os.Stderr))
	if err != nil {
		return err
	}
	defer client.Close()

	// // Run commands in container environment
	// out, err := client.
	// 	Container().
	// 	From("alpine:3.17").
	// 	WithExec([]string{"apk", "add", "curl"}).
	// 	WithExec([]string{"ls", "-la"}).
	// 	Stdout(ctx)
	// if err != nil {
	// 	return err
	// }
	// // Print result
	// fmt.Println(out)

	log.Info().Msg("Collecting parameters")
	entries, err := client.Host().Directory(".").Entries(ctx)
	if err != nil {
		log.Error().Msg(err.Error())
		return err
	}
	for _, entry := range entries {
		if entry == "parameters.json" {
			err := readAndPrintJSON(entry)
			if err != nil {
				fmt.Println("Error:", err)
			}
		}
	}

	return nil
}

func initLog() {
	zerolog.TimeFieldFormat = zerolog.TimeFormatUnix
	debug := flag.Bool("debug", false, "sets log level to debug")

	flag.Parse()

	// Default level
	zerolog.SetGlobalLevel(zerolog.InfoLevel)
	if *debug {
		zerolog.SetGlobalLevel(zerolog.DebugLevel)
	}

	log.Info().Msg("Running..")
}

// NOTE: For debugging purposes for now
func readAndPrintJSON(fileName string) error {
	// Open the JSON file
	file, err := os.Open(fileName)
	if err != nil {
		return err
	}
	defer file.Close()

	// Read the content of the file
	data, err := io.ReadAll(file)
	if err != nil {
		return err
	}

	// Create a map to unmarshal JSON data
	var jsonData map[string]interface{}

	// Unmarshal JSON data into the map
	err = json.Unmarshal(data, &jsonData)
	if err != nil {
		return err
	}

	// Print the content
	fmt.Printf("JSON Data:\n%+v\n", jsonData)

	return nil
}
