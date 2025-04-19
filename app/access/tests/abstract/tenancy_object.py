


class TenancyObject:
    """ Tests for checking TenancyObject """

    model = None
    """ Model to be tested """

    should_model_history_be_saved: bool = True
    """ Should model history be saved.

    By default this should always be 'True', however in special
    circumstances, this may not be desired.
    """


    # def test_history_save(self):
    #     """Confirm the desired intent for saving model history."""

    #     assert self.model.save_model_history == self.should_model_history_be_saved



    # @pytest.mark.skip(reason="to be written")
    # def test_edit_no_organization_fails(self):
    #     """ Devices must be assigned an organization

    #     Must not be able to edit an item without an organization
    #     """
    #     pass

