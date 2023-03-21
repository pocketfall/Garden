<html>
  <head>
    <meta charset= "utf-8">
    <title>BMI CALCULATOR PHP</title>
    <link rel= "stylesheet" href= "bmiStyling.css"/>
  </head>
  <body>
    <h1>BMI CALCULATOR WEBAPP</h1>
    <form action="bmi_calc.php" method="post">
      Weight: <input type="number" name="weight"/><br>
      Enter the unit of measure for it (lbs, kg): <input type="text" name="type_weight"/><br>
      Height: <input type="number" name="height"/><br>
      Enter the unit of measure for it (ft, m, cm): <input type="text" name="type_height"/><br>
      <input type="submit">
    </form>
    <h2>Result</h2>
    <?php
      function doConversion($numStuff, $typeStuff) {
        $typeVar = strtolower($typeStuff);
        switch ($typeVar) {
          case "lbs":
            $numStuff *= 0.45359237;
            break;
          case "cm":
            $numStuff = $numStuff / 100;
            break;
          case "ft":
            $numStuff *= 0.304;
            break;
          case "kg":
            break;
          case "m":
            break;
        }
        return $numStuff;
      }

      function getBmi($mass, $length) {
        $res = $mass / ($length ** 2);
        return $res;
      }

      function whereYouAre($bmi) {
        if ($bmi < 18.5) {
          return "Underweight";
        } else if (25 > $bmi && $bmi > 18.5) {
          return "Normal weight";
        } else if (30 > $bmi && $bmi > 25) {
          return "Overweight";
        } else if ($bmi > 30) {
          return "Obese";
        }
      }

      if (isset($_POST["weight"]) || isset($_POST["height"]) || isset($_POST["type_weight"]) || isset($_POST["type_height"])) {
        $weight = $_POST["weight"];
        $height = $_POST["height"];
        $typeWeight = $_POST["type_weight"];
        $typeHeight = $_POST["type_height"];

        $mass = doConversion($weight, $typeWeight);
        $length = doConversion($height, $typeHeight);

        $bmi = getBmi($mass, $length);
        $weightRange = whereYouAre($bmi);

        echo "<p>Your BMI is: $bmi</p>";
        echo "<p>That is: $weightRange</p>";
        echo "Thank you for using the BMI calculator";
      }
    ?>
  </body>
</html>
