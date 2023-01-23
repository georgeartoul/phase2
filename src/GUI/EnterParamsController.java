package GUI;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.URL;
import java.util.ResourceBundle;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Spinner;
import javafx.scene.control.SpinnerValueFactory;
import javafx.scene.control.TextField;
import javafx.scene.layout.AnchorPane;
import javafx.stage.Stage;

public class EnterParamsController implements Initializable {
	public static Stage primaryStage;
	FileWriter fw = null;
	BufferedWriter bw = null;
	PrintWriter pw = null;

	@FXML
	private Button nextBtn;

	@FXML
	private TextField rl1;

	@FXML
	private TextField sl1;

	@FXML
	private TextField sl2;

	@FXML
	private TextField rl2;

	@FXML
	void nextStep(ActionEvent event) throws Exception {
		int sl_1 = Integer.parseInt(sl1.getText()),
				sl_2 = Integer.parseInt(sl2.getText());
				
		double rl_1 = Double.parseDouble(rl1.getText()),rl_2 = Double.parseDouble(rl2.getText());

		fw = new FileWriter("C:\\Users\\franc\\eclipse-workspace\\Phase2\\src\\GUI\\DataBase.txt", false);
		bw = new BufferedWriter(fw);
		pw = new PrintWriter(bw);
		pw.println(rl_1 + "," + sl_1);
		pw.println(rl_2 + "," + sl_2);
		pw.flush();

		SetStrategyController setStrategyController = new SetStrategyController();
    	setStrategyController.start(primaryStage);
	}

	public void start(Stage primaryStage) throws Exception {
		EnterParamsController.primaryStage = primaryStage;
		Parent root = FXMLLoader.load(getClass().getResource("/GUI/EnterParams.fxml"));
		Scene scene = new Scene(root);
		primaryStage.setTitle("Roads Parameters");
		primaryStage.setScene(scene);
		primaryStage.show();

	}

	@Override
	public void initialize(URL arg0, ResourceBundle arg1) {
		// TODO Auto-generated method stub

	}

}
