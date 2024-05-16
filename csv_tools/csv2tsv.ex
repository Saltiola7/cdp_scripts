defmodule CsvToTsv do
  def convert(input_path, output_path) do
    start_time = System.monotonic_time(:millisecond)

    input_path
    |> File.stream!()
    |> Stream.map(&String.replace(&1, ~r/","/u, "\t"))
    |> Stream.into(File.stream!(output_path, [:write]))
    |> Stream.run()

    end_time = System.monotonic_time(:millisecond)
    elapsed_time = end_time - start_time

    IO.puts("Conversion took #{elapsed_time} milliseconds.")
  end
end

input_path = "/Users/tis/foam/cdp/data/turo.tsv"
output_path = "/Users/tis/foam/cdp/data/turoex.tsv"

CsvToTsv.convert(input_path, output_path)
