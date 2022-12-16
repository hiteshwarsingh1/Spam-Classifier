<h3>Spam Filter</h3>
<hr>
		<p>The dataset we will be using is a subset of 2005 TREC Public Spam Corpus. It contains a <code>training set</code> and a <code>test set</code>. Both files use the same format: each line represents the space-delimited properties of an email, with the first one being the email ID, the second one being whether it is a spam or ham (non-spam), and the rest are words and their occurrence numbers in this email. In preprocessing, non-word characters have been removed, and features selected similar to what Mehran Sahami did in his <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/1998/01/junkfilter.pdf">original paper</a> using Naive Bayes to classify spams.</p>
		<h4><u>Dataset</u></h4>
    <p>The data set can be downloaded from <code><a href="project05/data.zip">here</a></code>.</p>
		<p>Features selected makes learning much easier, but it also throws out useful information. For example, exclamation mark (!) often occurs in spams. Even the format of email sender matters: in the case when an email address appears in the address book, a typical email client will replace it with the contact name, which means that the email is unlikely to be a spam (unless, of course, you are a friend of the spammer!). Sahami's paper talked about a few such features he had used in his classifier. </p>
		
		<p>Usage: python q2_classifier.py -f1 <train_dataset> -f2 <test_dataset> -o <output_file>

        Where:

        <train_dataset> and <test_dataset> contain space delimited properties of an email
        <output_file> is a csv file containing the predicted labels for the test dataset</p>